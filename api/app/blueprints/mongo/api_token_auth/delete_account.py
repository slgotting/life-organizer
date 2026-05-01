from flask import request, current_app, render_template
from app.blueprints.mongo.api_token_auth import bp
from app.blueprints.mongo.api_token_auth.models import User
from app.blueprints.mongo.api_token_auth.forms import ResetPasswordForm
from app.blueprints.mongo.api_token_auth.helpers import get_user_by_email, get_account_deletion_url, \
    get_user_from_request_headers
from app.blueprints.email.email import send_email
from app.blueprints.mongo.api_token_auth.token_verification import verify_token


@bp.route('/delete_account', methods=['DELETE'])
@verify_token
def delete_account():
    user = get_user_from_request_headers(request.headers)

    try:
        user.delete()
        return {'success': "Account deleted! We're sorry to see you go :("}, 200
    except:
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500
