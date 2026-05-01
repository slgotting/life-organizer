from app.blueprints.subscription.providers.stripe import Stripe
from app.blueprints.subscription.providers.solana import Solana
from app.blueprints.subscription.providers.test import TestProvider
from app.blueprints.subscription.plan_types import FreeSubscriptionPlan, \
    BasicSubscriptionPlan, CultivatingSubscriptionPlan, LearnedSubscriptionPlan, \
    LifetimeSubscriptionPlan

SUBSCRIPTION_PLAN_PRICE_MAP = {
    'Free': 0, # |UPDATE_ME|
    'Basic': 4, # |UPDATE_ME|
    'Cultivating': 8, # |UPDATE_ME|
    'Learned': 12, # |UPDATE_ME|
    'Lifetime': 30, # |UPDATE_ME|
}

SUBSCRIPTION_PLAN_TYPE_STRINGS = [ 'Free', 'Basic', 'Cultivating', 'Learned', 'Lifetime'] # |UPDATE_ME|
SUBSCRIPTION_PLAN_TYPES = {
    'Free': FreeSubscriptionPlan, # |UPDATE_ME|
    'Basic': BasicSubscriptionPlan, # |UPDATE_ME|
    'Cultivating': CultivatingSubscriptionPlan, # |UPDATE_ME|
    'Learned': LearnedSubscriptionPlan, # |UPDATE_ME|
    'Lifetime': LifetimeSubscriptionPlan, # |UPDATE_ME|
}

ONE_TIME_OPTIONS = {
    'Lifetime': LifetimeSubscriptionPlan # |UPDATE_ME|
}

PROVIDER_MAP = {
    'stripe': Stripe,
    'solana': Solana,
    'test': TestProvider
}
DEFAULT_SUBSCRIPTION_PROVIDERS = {
    'Free': {
        'customer_id': 'cust_123',
        'subscription_id': 'sub_123',
        'plan': 'Free',
        'status': 'Active',
        'canceled': False,
        'start': None,
        'end': None,
    },
    'Stripe': {
        'customer_id': '',
        'subscription_id': '',
        'plan': '',
        'status': 'Inactive',
        'canceled': False,
        'start': None,
        'end': None,
    },
    'Solana': {
        'customer_id': '',
        'subscription_id': '',
        'plan': '',
        'status': 'Inactive',
        'canceled': False,
        'start': None,
        'end': None,
    },
}