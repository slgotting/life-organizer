import datetime
from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPE_STRINGS, SUBSCRIPTION_PLAN_PRICE_MAP

# def format_timestamp(timestamp, format="%b %-d, %Y - %H:%M:%S"):
def format_timestamp(timestamp, format="%b %-d, %Y"):
    return datetime.datetime.fromtimestamp(timestamp).strftime(format)

def subscription_just_renewed(old_end_timestamp, new_start_timestamp):
    return old_end_timestamp == new_start_timestamp

def get_and_convert_status_for_subscription(data, provider="Stripe"):
    '''
        Basically converts a provider's status into something we operate with.

        Currently that means either "Active" or "Inactive"

        "Active" meaning allow access to the plan's access level, credits, etc...
        "Inactive" meaning do not allow access to it
    '''
    if provider == "Stripe":
        inactive_status_types = ["incomplete", "incomplete_expired", "past_due", "canceled", "unpaid", "paused"]
        active_status_types = ["trialing", "active"]
        return "Active" if data['status'] in active_status_types else "Inactive"

def build_prorations(current_plan, timestamp_end, period="monthly"):
    if current_plan == "Free":
        return SUBSCRIPTION_PLAN_PRICE_MAP

    if period == "monthly":
        time_left_ratio = (timestamp_end - datetime.datetime.utcnow().timestamp()) / 2678400 # num seconds in 31 day month

    return {
        plan: (SUBSCRIPTION_PLAN_PRICE_MAP[plan] - SUBSCRIPTION_PLAN_PRICE_MAP[current_plan]) * time_left_ratio
        for plan in SUBSCRIPTION_PLAN_TYPE_STRINGS
    }
