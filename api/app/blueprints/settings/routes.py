
import time
from app import sql_db as db
from flask import request, jsonify, send_file, current_app
from app.blueprints.api import bp
from app.blueprints.mongo.api_token_auth.token_verification import verify_token
from app.blueprints.mongo.api_token_auth.helpers import get_user_by_id, get_user_from_request_headers
from app.blueprints.api.helpers import build_jwt_url, decode_jwt, decode_jwt_no_signature_check
from app.blueprints.helpers.forms import build_form_errors_string
from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPES


@bp.route('/settings', methods=["GET"])
@verify_token
def settings():
    try:
        user = get_user_from_request_headers(request.headers)
        time.sleep(0.5)
        return jsonify(user.settings), 200
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

@bp.route('/update_settings', methods=["POST"])
@verify_token
def update_settings():
    try:
        user = get_user_from_request_headers(request.headers)
        user.update_settings(request.form)
        return {'success': True}, 200
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500
