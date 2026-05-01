from flask import Blueprint, current_app
from app.blueprints.payments_stripe.event_handling import Event

bp = Blueprint(
    'stripe',
    __name__,
    template_folder='templates',
    url_prefix='/stripe'
)

@bp.before_request
def handle_event_clearing():
    if current_app.request_count % 10000 == 0 or current_app.request_count % 10000 == 1:
        Event.delete_all()

from app.blueprints.payments_stripe import webhooks
