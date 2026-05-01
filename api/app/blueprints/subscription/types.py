from typing import TypedDict

SubscriptionProvider = str

ProductID = str
PriceID = str

Active = str
Inactive = str

Unlimited = str

SubscriptionAccess = dict
# SubscriptionAccess = {
#     'Custom Notifs': bool,
#     'Dashboard Access': bool,
#     'Advertisements': bool,
#     'Credits': {
#         'gpt-3_5': [int|Unlimited], # IMPORTANT FOR MONGOENGINE - CANNOT HAVE A DOT IN THE NAME, ELSE THE PARSER VIEWS IT AS A COLLECTION
#         'gpt-4o': [int|Unlimited],
#     }
# }

SubscriptionDetails = dict
# SubscriptionDetails = {
#     'plan': str,
#     'status': [Active|Inactive],
#     'access': SubscriptionAccess,
#     'renewal_date': str,
#     'canceled': bool,
# }

SubscriptionState = dict
# SubscriptionState = {
#     'customer_id': str,
#     'subscription_id': str,
#     'plan': str,
#     'status': [Active|Inactive],
#     'canceled': bool, # if this exists then we are 'canceled' though not technically 'canceled' in stripes perception
#     'start': [int|float],
#     'end': [int|float],
# }
