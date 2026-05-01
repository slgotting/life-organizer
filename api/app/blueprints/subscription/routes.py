import stripe
import datetime
from flask import request, jsonify, current_app
from app.blueprints.subscription import bp
from app.blueprints.mongo.api_token_auth.token_verification import verify_token
from app.blueprints.mongo.api_token_auth.helpers import get_user_from_request_headers
from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPES, ONE_TIME_OPTIONS, \
    SUBSCRIPTION_PLAN_PRICE_MAP
from app.blueprints.subscription.helpers import build_prorations


@bp.route('/details', methods=["GET"])
@verify_token
def details():
    try:
        user = get_user_from_request_headers(request.headers)
        details = user.subscription_details
        details['plan_types'] = [
            {
                'plan': string,
                'access': plan().initial_access_data
            }
            for (string, plan) in SUBSCRIPTION_PLAN_TYPES.items()
        ]
        details['plan_type_prorated_prices'] = build_prorations(details['plan'], user.best_active_subscription_state['end'])
        details['plan_type_prices'] = SUBSCRIPTION_PLAN_PRICE_MAP
        details['lifetime_access'] = True if user.lifetime_access else False
        return jsonify(details), 200
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

@bp.route('/stripe-customer-portal-session', methods=["POST"])
@verify_token
def stripe_customer_portal_session():
    try:
        user = get_user_from_request_headers(request.headers)
        session = stripe.billing_portal.Session.create(
            customer=user.subscription_providers['Stripe']['customer_id'],
            return_url=f"{current_app.config.get('CLIENT_URI')}/account-settings",
        )
        return {'url': session.url}, 200
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

@bp.route('/purchase_lifetime_access', methods=["POST"])
@verify_token
def purchase_lifetime_access():
    user = get_user_from_request_headers(request.headers)
    if request.form['paymentType'] == "Credit Card":

        customer_id = user.subscription_providers.get('Stripe').get('customer_id')
        if not customer_id:
            customer = stripe.Customer.create(email=user.email)
            customer_id = customer.id
            user.subscription_providers['Stripe']['customer_id'] = customer_id
            user.save()

        session = stripe.checkout.Session.create(
            customer=customer_id,
            success_url=current_app.config.get('CLIENT_URI') + f'/lifetime-success',
            cancel_url=current_app.config.get('CLIENT_URI') + '/account-settings?toast=subscription-request-canceled',
            mode='payment',
            line_items=[{
                'price': ONE_TIME_OPTIONS['Lifetime']().get_price_id("one_time", "Stripe"),
                'quantity': 1,
            }]
        )
    return jsonify(url=session.url)


@bp.route('/change_plan', methods=["POST"])
@verify_token
def change_plan():
    from app.blueprints.subscription.subscription_plan import SubscriptionPlan
    try:
        user = get_user_from_request_headers(request.headers)
        new_plan = SubscriptionPlan.from_string(request.form['plan'])
        current_plan = user.subscription_plan
        active_provider, subscription_state = user.get_best_active_subscription()

        if current_plan > new_plan:
            if request.form['paymentType'] == "Credit Card":
                try:
                    customer_id = user.subscription_providers['Stripe']['customer_id']
                    sub_id = user.subscription_providers['Stripe']['subscription_id']
                    subscription = stripe.Subscription.retrieve( sub_id )

                    if subscription['cancel_at_period_end']: # means user canceled and we have to resume
                        stripe.Subscription.modify(
                            sub_id,
                            cancel_at_period_end=False
                        )

                    stripe.Subscription.modify(
                        sub_id,
                        items=[{
                            'id': subscription['items']['data'][0]['id'],
                            'price': new_plan.get_price_id("monthly", "Stripe"),
                        }],
                        proration_behavior='none',
                    )
                    return {'success': f'Successfully downgraded subscription to {new_plan.plan_string}. You will still have "{current_plan.plan_string}" access until the plan renews.'}
                except:
                    current_app.logger.exception('An unknown error occurred')
                    return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

        elif current_plan < new_plan:
            # upgrade
            if request.form['paymentType'] == "Credit Card":
                if not active_provider or active_provider == "Free":
                    customer_id = user.subscription_providers.get('Stripe').get('customer_id')

                    if not customer_id:
                        customer = stripe.Customer.create(email=user.email)
                        customer_id = customer.id
                        user.subscription_providers['Stripe']['customer_id'] = customer_id
                        user.save()

                    session = stripe.checkout.Session.create(
                        customer=customer_id,
                        success_url=current_app.config.get('CLIENT_URI') + f'/subscribe-success?type={request.form["plan"]}',
                        cancel_url=current_app.config.get('CLIENT_URI') + '/account-settings?toast=subscription-request-canceled',
                        mode='subscription',
                        line_items=[{
                            'price': new_plan.get_price_id("monthly", "Stripe"),
                            'quantity': 1,
                        }]
                    )

                    return jsonify(url=session.url)

                elif active_provider == "Stripe":
                    try:
                        customer_id = user.subscription_providers['Stripe']['customer_id']
                        sub_id = user.subscription_providers['Stripe']['subscription_id']
                        subscription = stripe.Subscription.retrieve( sub_id )
                        if subscription['cancel_at_period_end']: # means user canceled and we have to resume
                            stripe.Subscription.modify(
                                sub_id,
                                cancel_at_period_end=False
                            )
                        subscription = stripe.Subscription.modify(
                            sub_id,
                            items=[{
                                'id': subscription['items']['data'][0]['id'],
                                'price': new_plan.get_price_id("monthly", "Stripe"),
                            }],
                            proration_behavior='always_invoice',
                        )
                        return {'success': f'Successfully upgraded subscription to {new_plan.plan_string}!'}
                    except:
                        current_app.logger.exception('An unknown error occurred')
                        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

                    # upgrade plan by creating a prorated upgrade

                elif active_provider == "Solana":
                    pass

        else:
            # LOGGING OPPORTUNITY - log user who sent a request directly to this endpoint
            current_app.logger.exception('User tried to change to the same plan type, meaning they sent the request manually')
            return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

        # url = user.change_plan(request.form['plan'])
        return {'success': True}, 200
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500


@bp.route('/cancel_plan', methods=["POST"])
@verify_token
def cancel_plan():
    try:
        user = get_user_from_request_headers(request.headers)
        user.cancel_subscription(provider="Stripe")
        return jsonify(success=True), 200
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500