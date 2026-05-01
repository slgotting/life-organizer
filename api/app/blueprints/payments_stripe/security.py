import stripe
from flask import current_app

def verify_signature(request):
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
        event = stripe.Webhook.construct_event(
            payload, sig_header, secret
        )
    except ValueError as e:
        # Invalid payload
        return False
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return False
    return True
