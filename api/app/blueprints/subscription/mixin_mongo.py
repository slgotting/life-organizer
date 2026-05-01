import datetime
import stripe
import mongoengine as me
from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPES, \
    PROVIDER_MAP, DEFAULT_SUBSCRIPTION_PROVIDERS, SUBSCRIPTION_PLAN_TYPE_STRINGS
from app.blueprints.subscription.helpers import format_timestamp, \
    get_and_convert_status_for_subscription
from app.blueprints.subscription.providers.provider import Provider
from app.blueprints.subscription.subscription_plan import SubscriptionPlan
from app.blueprints.subscription.plan_types import FreeSubscriptionPlan
from app.blueprints.subscription.types import SubscriptionAccess, SubscriptionDetails, \
    SubscriptionState, SubscriptionProvider
from typing import Tuple

MODEL_ORDER = [
    'gpt-3_5', # IMPORTANT FOR MONGOENGINE - CANNOT HAVE A DOT IN THE NAME, ELSE THE PARSER VIEWS IT AS A COLLECTION
    'gpt-4o',
]

class SubscriptionMixin:
    subscription_access = me.DictField(default=FreeSubscriptionPlan().get_initial_access_data())
    subscription_providers = me.DictField(default=DEFAULT_SUBSCRIPTION_PROVIDERS)

    # store the provider and transaction id like such: Stripe-<id>
    lifetime_access = me.StringField(default="")

    def __init__(self):
        utc_now = datetime.datetime.utcnow()
        state = self.best_active_subscription_state
        plan = SubscriptionPlan.from_string(state['plan'])
        if 'Stripe' not in self.best_active_subscription_provider:
            self.subscription_providers = DEFAULT_SUBSCRIPTION_PROVIDERS
        if not self.subscription_access:
            self.subscription_access = plan.initial_access_data
        if plan.plan_string == "Free":
            if not state['end'] or state['end'] < utc_now.timestamp():
                state['start'] = utc_now.timestamp()
                state['end'] = (utc_now + datetime.timedelta(days=30)).timestamp()

        self.save()

    @classmethod
    def get_user_by_subscription_provider_customer_id(cls, customer_id, provider="Stripe"):
        if provider == "Stripe":
            user = cls.objects(subscription_providers__Stripe__customer_id=customer_id).first()
        if provider == "Solana":
            user = cls.objects(subscription_providers__Solana__customer_id=customer_id).first()
        return user

    @property
    def subscription_plan(self):
        provider, state = self.get_best_active_subscription()
        if provider:
            return SUBSCRIPTION_PLAN_TYPES[state['plan']](state)
        else:
            return SUBSCRIPTION_PLAN_TYPES['Free']()

    @property
    def subscription_details(self) -> SubscriptionDetails:
        state = self.best_active_subscription_state
        return {
            'plan': state['plan'],
            'status': state['status'],
            'access': self.subscription_access,
            'renewal_date': format_timestamp(state['end']) if state['plan'] != 'Lifetime' else 'Lifetime',
            'canceled': state['canceled'],
        }

    def update_subscription_access(self, data_object) -> SubscriptionAccess:
        self.subscription_access = data_object
        self.save()

    def update_subscription_state(self, plan_string, data_object, provider="Stripe"):
        if provider == "Stripe":
            state = {
                'customer_id': data_object["customer"],
                'subscription_id': data_object["id"],
                'plan': plan_string,
                'status': get_and_convert_status_for_subscription(data_object, provider),
                'canceled': True if data_object["cancel_at_period_end"] else False, # if this exists then we are 'canceled' though not technically 'canceled' in stripes perception
                'start': data_object["current_period_start"],
                'end': data_object["current_period_end"],
            }
        self.subscription_providers[provider] = state
        self.save()

    @property
    def best_active_subscription_provider(self) -> SubscriptionProvider:
        # if a subscription is active, return the provider
        return self.get_best_active_subscription()[0]

    @property
    def best_active_subscription_state(self) -> SubscriptionState:
        # if a subscription is active, return the provider
        return self.get_best_active_subscription()[1]

    def get_best_active_subscription(self) -> Tuple[str, SubscriptionState]:
        ''' ACTIVE HERE MEANS THE CURRENT TIMESTAMP IS LESS THAN THE SUBSCRIPTION END;
                NOT ACTIVE AS IN THE PROVIDER'S STATE; A "Canceled" state could still be "active"

            Returns (provider_string, provider_state) with best active subscription; empty string if none active
        '''
        # if self.lifetime_access:
        #     return ('Lifetime', SubscriptionPlan.from_string(SubscriptionPlan.PLAN_ORDER[-1]).get_initial_access_data())

        highest = ('Free', DEFAULT_SUBSCRIPTION_PROVIDERS["Free"]) # (provider, plan)
        highest_plan = FreeSubscriptionPlan()
        for provider, state in self.subscription_providers.items():
            plan_string = state.get("plan")
            if not plan_string: continue
            plan = SubscriptionPlan.from_string(plan_string)
            if state["status"] == "Active":
                if not highest[1] or plan > highest_plan:
                    highest = (provider, state)
                    highest_plan = plan
        return highest

    def get_best_model_option(self) -> str:
        query_credit_options = self.subscription_access['Credits']
        for model in reversed(MODEL_ORDER):
            if model in query_credit_options:
                query_credits = query_credit_options[model]
                if isinstance(query_credits, int) and query_credits > 0:
                    return model
                elif isinstance(query_credits, str) and query_credits == 'unlimited':
                    return model
        return None

    def get_credits_left(self, key: str) -> int:
        credits = self.subscription_access["Credits"].get(key)
        return credits if credits else 0

    def decrement_credits(self, key: str, num_credits: int = 1, preflight_check=True) -> bool:
        credits_left = self.get_credits_left(key)
        if credits_left == "unlimited":
            return True

        if preflight_check:
            if self.get_credits_left(key) < num_credits:
                return False

        self.subscription_access["Credits"][key] = self.subscription_access["Credits"][key] - num_credits
        self.save()
        # self.update(Credits=self.subscription_access["Credits"])
        return True

    def set_credits(self, key: str, num: int | str) -> bool:
        self.subscription_access["Credits"][key] = num
        self.save()
        return True

    def has_access(self, attr: str):
        if attr not in self.subscription_access:
            return False
        else:
            return self.subscription_access[attr]

    def cancel_subscription(self, provider="Stripe"):
        if provider == "Stripe":
            stripe.Subscription.modify(
                self.subscription_providers['Stripe']['subscription_id'],
                cancel_at_period_end=True,
            )
            self.subscription_providers["Stripe"]["canceled"] = True
            self.save()
            return True

    def give_lifetime_access(self, event_id, provider="Stripe"):
        self.subscription_providers[provider]['plan'] = "Lifetime"
        self.subscription_providers[provider]['status'] = "Active"
        self.subscription_providers[provider]['canceled'] = False
        self.subscription_providers[provider]['start'] = 0
        self.subscription_providers[provider]['end'] = 999999999999
        self.lifetime_access = f"{provider}-{event_id}"

        new_plan = SUBSCRIPTION_PLAN_TYPES["Lifetime"]()
        self.update_subscription_access(new_plan.initial_access_data)

        self.save()
        return True
