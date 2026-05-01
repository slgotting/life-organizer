import stripe
from flask import request, current_app
from app.blueprints.payments_stripe.event_handling import Event
from app.blueprints.payments_stripe.security import verify_signature
from app.blueprints.subscription.types import ProductID
from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPES
from app.blueprints.subscription.helpers import subscription_just_renewed, \
    get_and_convert_status_for_subscription
from app.blueprints.subscription.subscription_plan import SubscriptionPlan
from app.blueprints.mongo.api_token_auth.models import User
from app.blueprints.helpers.config import get

from app.blueprints.payments_stripe import bp

def get_product_from_checkout_session(session_id) -> ProductID:
    line_items = stripe.checkout.Session.list_line_items(session_id)

    for item in line_items['data']:
        product_id = item['price']['product']
        return product_id

@bp.route('/webhook', methods=["POST"])
def webhook():
    verified = verify_signature(request)

    if not verified:
        current_app.logger.warning("Attempted webhook spoof")
        return {}

    json = request.json

    event = json['type']
    data = json['data']['object']
    customer_id = data['customer']

    if event == "checkout.session.completed":
        # the only option here is that it was the lifetime access option currently
        session_id = data['id']
        if data["mode"] == "payment":
            if data["payment_status"] == "paid":
                product = get_product_from_checkout_session(session_id)
                if get("STRIPE_PRODUCT_PLAN_MAP").get(product) == "Lifetime":
                    user = User.get_user_by_subscription_provider_customer_id(customer_id, "Stripe")
                    user.give_lifetime_access(data['id'], "Stripe")

    elif event == "customer.subscription.updated":
        product = data['plan']['product']
        plan_str = get("STRIPE_PRODUCT_PLAN_MAP").get(product)
        new_plan = SubscriptionPlan.from_string(plan_str)
        user = User.get_user_by_subscription_provider_customer_id(customer_id, "Stripe")

        best_provider, state = user.get_best_active_subscription()

        existing_plan = SubscriptionPlan.from_string(state.get("plan"))

        current_period_start = state.get("start")
        current_period_end = state.get("end")

        if new_plan > existing_plan:
            user.update_subscription_access(new_plan.initial_access_data)
            user.update_subscription_state(new_plan.plan_string, data, "Stripe")
        elif new_plan < existing_plan:
            # i think i do nothing here
            # maybe check the period end and start?
            # or i think listening for a subscription renewal event (if it exists) is better
            # because then on the subscription end, i will set their plan to the initial state
            # of whichever plan was sent in the hook
            new_status = get_and_convert_status_for_subscription(data, provider="Stripe")
            if new_status != state["status"]: # for handling our representation of how we store status
                if new_status == "Active":
                    user.update_subscription_access(new_plan.initial_access_data)

            user.update_subscription_state(new_plan.plan_string, data, "Stripe")

        else:
            if subscription_just_renewed(current_period_end, data['current_period_start']):
                user.update_subscription_access(new_plan.initial_access_data)
                user.update_subscription_state(new_plan.plan_string, data, "Stripe")
            else: # not sure why an update was called?
                # i dont think we want to reinitialize the access here but i could be wrong
                # user.update_subscription_access(new_plan.initial_access_data)
                user.update_subscription_state(new_plan.plan_string, data, "Stripe")

    elif event == "customer.subscription.deleted":
        product = data['plan']['product']
        plan_str = get("STRIPE_PRODUCT_PLAN_MAP").get(product)
        new_plan = SubscriptionPlan.from_string(plan_str)
        user = User.get_user_by_subscription_provider_customer_id(customer_id, "Stripe")

        provider, state = user.get_best_active_subscription()
        plan_str = state.get("plan")

        if provider == "Stripe" or not plan_str or plan_str == "Free":
            new_plan = SUBSCRIPTION_PLAN_TYPES["Free"]()
        else:
            new_plan = SUBSCRIPTION_PLAN_TYPES[plan_str]()
        user.update_subscription_state("Free", data, provider="Stripe")
        user.update_subscription_access(new_plan.initial_access_data)

    if not Event.event_processed(data['id']):
        event = Event(event_id=data['id'])

        try:
            event.save()
        except:
            pass

    return {}