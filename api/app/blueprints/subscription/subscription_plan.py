'''
This file provides the mappings to each plans attributes
'''
from abc import ABC, abstractmethod

MODEL_ORDER = [
    'gpt-3_5',
    'gpt-4o'
]

class SubscriptionPlan(ABC):
    PLAN_ORDER = [
        "Free",
        "Basic", # |UPDATE_ME|
        "Cultivating", # |UPDATE_ME|
        "Learned", # |UPDATE_ME|
        "Lifetime", # |UPDATE_ME|
    ]

    def __init__(self, access=None):
        if access:
            self.access = access
        else:
            self.access = self.get_initial_access_data()

    @property
    def initial_access_data(self):
        return self.get_initial_access_data()

    @staticmethod
    def from_string(string):
        from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPES
        return SUBSCRIPTION_PLAN_TYPES[string]()

    @property
    @abstractmethod
    def plan_string(self):
        ...

    @property
    def price_ids(self):
        from app.blueprints.subscription.constants import STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP
        return {
            'Stripe': STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP[self.plan_string]
        }

    def get_price_id(self, period="monthly", provider="Stripe"):
        try:
            return self.price_ids[provider][period]
        except KeyError:
            return f"Price ID not found for Provider: {provider} - Period: {period}"

    @property
    def rank(self):
        return self.PLAN_ORDER.index(self.plan_string)

    @classmethod
    def init_from_current_access(cls, access):
        instance = cls()
        instance.access = access
        return instance

    @abstractmethod
    def get_initial_access_data(self):
        ...

    def has_access(self, attr) -> bool | None:
        return self.access.get(attr)

    def export_initial_access_data(self):
        return self.get_initial_access_data()

    def __gt__(self, other_plan):
        return self.rank > other_plan.rank

    def __lt__(self, other_plan):
        return self.rank < other_plan.rank

    def __eq__(self, other_plan):
        return self.rank == other_plan.rank

    def __ne__(self, other_plan):
        return self.rank != other_plan.rank
