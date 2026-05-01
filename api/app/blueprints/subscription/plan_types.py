
from app.blueprints.subscription.subscription_plan import SubscriptionPlan

class FreeSubscriptionPlan(SubscriptionPlan):
    def __init__(self, access=None):
        super().__init__(access=access)

    @property
    def plan_string(self):
        return 'Free'

    def get_initial_access_data(self):
        return {
            'Custom Notifs': False,
            'Dashboard Access': False,
            'Advertisements': True,
            'Credits': {
                'gpt-3_5': 20,
                'gpt-4o': False,
            }
        }

class BasicSubscriptionPlan(SubscriptionPlan):
    def __init__(self, access=None):
        super().__init__(access=access)

    @property
    def plan_string(self):
        return 'Basic'

    def get_initial_access_data(self):
        return {
            'Custom Notifs': False,
            'Dashboard Access': True,
            'Advertisements': False,
            'Credits': {
                'gpt-3_5': 'unlimited',
                'gpt-4o': False,
            }
        }

class CultivatingSubscriptionPlan(SubscriptionPlan):
    def __init__(self, access=None):
        super().__init__(access=access)

    @property
    def plan_string(self):
        return 'Cultivating'

    def get_initial_access_data(self):
        return {
            'Custom Notifs': True,
            'Dashboard Access': True,
            'Advertisements': False,
            'Credits': {
                'gpt-3_5': 'unlimited',
                'gpt-4o': '200',
            }
        }

class LearnedSubscriptionPlan(SubscriptionPlan):
    def __init__(self, access=None):
        super().__init__(access=access)

    @property
    def plan_string(self):
        return 'Learned'

    def get_initial_access_data(self):
        return {
            'Custom Notifs': True,
            'Dashboard Access': True,
            'Advertisements': False,
            'Credits': {
                'gpt-3_5': 'unlimited',
                'gpt-4o': 'unlimited',
            }
        }

class LifetimeSubscriptionPlan(LearnedSubscriptionPlan):
    def __init__(self, access=None):
        super().__init__(access=access)

    @property
    def plan_string(self):
        return 'Lifetime'

    # defined by Learned
    # def get_initial_access_data(self):
