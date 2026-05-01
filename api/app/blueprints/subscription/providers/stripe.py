import stripe
from flask import jsonify, current_app
from app.blueprints.subscription.providers.provider import Provider, \
    CustomerID
from typing import Tuple


class Stripe(Provider):

    def __init__(self, customer_id, subscription_id) -> None:
        # call parent classes method
        super().__init__(customer_id, subscription_id)

    @staticmethod
    def create_customer(email) -> CustomerID:
        customer = stripe.Customer.create(email=email)
        return customer.id

    @staticmethod
    def get_or_create_customer(customer_id, email):
        try:
            customer = Stripe.get_customer(customer_id)
            customer_id = customer.id
        except:
            pass

        if not customer_id:
            customer = Stripe.create_customer(email)
            customer_id = customer.id
        return customer_id

    def get_customer(self, customer_id) -> object:
        return stripe.Customer.retrieve(customer_id)

    def get_subscription(self) -> object:
        return stripe.Subscription.retrieve(self.subscription_id)

    def get_plan(self):
        from app.blueprints.subscription.constants import STRIPE_PRODUCT_PLAN_MAP
        return STRIPE_PRODUCT_PLAN_MAP[self.get_subscription()['plan']['product']]

    def downgrade_plan(self):
        pass

    def upgrade_plan(self, new_plan) -> Tuple[str, str]:
        checkout_session = self.create_checkout_session(new_plan)
        return checkout_session.url, checkout_session.id

    def create_checkout_session(self, plan: str) -> stripe.checkout.Session:
        domain_url = current_app.config.get('SERVER_URI')
        # not used, see routes this should break
        # from app.blueprints.subscription.constants import STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP
        # price_id = STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP[plan]['monthly']

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/stripe/checkout-success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/stripe/checkout-canceled',
                mode='subscription',
                automatic_tax={'enabled': True},
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }]
            )

            # attach the checkout sessions id to the user

            # in the webhook, listen for checkout.session.completed and then bind the relevant
            # identifiers to that user:
            #   - "subscription" (the subscription id)
            #   - "customer" (the customer id)
            # think this is all for now

            # then register the event id of the webhook as seen in the database
            #   iterating over them before processing any new webhook events
            #   clear these out once every 100000? requests or so and on app startup

            return checkout_session
        except Exception as e:
            return jsonify(error=str(e)), 403

    def update_subscription(self, new_plan):
        # from app.blueprints.subscription.constants import STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP
        # price_id = STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP[new_plan]['monthly']

        subscription = stripe.Subscription.retrieve(self.subscription_id)
        # we must extract the subscription item id from our query in order to update that
        item_id = subscription['items']['data'][0]['id']
        stripe.Subscription.modify(
            self.subscription_id,
            items=[{"id": item_id, "price": price_id}],
            # If you want to charge for an upgrade immediately, pass proration_behavior as always_invoice to create prorations, automatically invoice the customer for those proration adjustments, and attempt to collect payment. If you pass create_prorations, the prorations are created but not automatically invoiced. If you want to bill the customer for the prorations before the subscription's renewal date, you need to manually [invoice the customer](https://stripe.com/docs/api/invoices/create).
            proration_behavior="always_invoice"
        )

    def create_subscription(self, plan):
        # from app.blueprints.subscription.constants import STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP
        # price_id = STRIPE_SUBSCRIPTION_PLAN_PRICE_MAP[plan]['monthly']
        # not used, just generates an invoice but doesnt give a stripe url
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