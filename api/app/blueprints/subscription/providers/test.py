import random
import stripe
from flask import jsonify, current_app
from app.blueprints.subscription.providers.provider import Provider, \
    CustomerID
from typing import Tuple

def generate_random_id():
    return '{:04d}'.format(random.randint(0, 9999))

class TestProvider(Provider):

    def __init__(self, customer_id, subscription_id) -> None:
        # call parent classes method
        super().__init__(customer_id, subscription_id)

    @staticmethod
    def create_customer(email) -> CustomerID:
        return f'cust_{generate_random_id()}'

    def get_customer(self, customer_id) -> object:
        return {
            'id': f'cust_{generate_random_id()}',
            'sub_id': f'sub_{generate_random_id()}',
            'plan': self.get_plan()
        }

    def downgrade_plan(self):
        pass

    def get_plan(self):
        return random.choice(["Free", "Basic", "Cultivating", "Learned"])

    def upgrade_plan(self, new_plan) -> Tuple[str, str]:
        return f'http://localhost:5000/test/upgrade-plan/{new_plan}', 'upgrade_123'

    def update_subscription(self, new_plan):
        pass

    def create_subscription(self, plan):
        try:
            # Create the subscription. Note we're using
            # expand here so that the API will return the Subscription's related
            # latest invoice, and that latest invoice's payment_intent
            # so we can collect payment information and confirm the payment on the front end.

            # Create the subscription
            subscription = stripe.Subscription.create(
                customer=self.customer_id,
                items=[{
                    'price': price_id,
                }],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )
            return {
                'subscriptionId': subscription.id,
                'clientSecret': subscription.latest_invoice.payment_intent.client_secret
            }
        except Exception as e:
            return jsonify(error={'message': e.user_message}), 400

    def to_json(self, customer_id):
        # /v1/customers/:id
        return {
            'customer_id': '',
            'subscription_id': '',
            'plan': '',
            'credits': '',
        }

    def export_json(self, customer_id):
        return self.to_json(customer_id)