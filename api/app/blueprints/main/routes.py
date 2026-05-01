import time
from app import sql_db as db
from flask import request, jsonify, send_file, current_app
from app.blueprints.api import bp
from app.blueprints.mongo.api_token_auth.token_verification import verify_token
from app.blueprints.mongo.api_token_auth.helpers import get_user_by_id, get_user_from_request_headers
from app.blueprints.api.helpers import build_jwt_url, decode_jwt, decode_jwt_no_signature_check
from app.blueprints.helpers.forms import build_form_errors_string
from app.blueprints.subscription.constants import SUBSCRIPTION_PLAN_TYPES


@bp.route('/', methods=["GET"])
def home():
    return 'beeboop'

@bp.route('/favicon.ico', methods=["GET"])
def favicon():
    return send_file('static/favicon.png')
