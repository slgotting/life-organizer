import time
from flask import request, jsonify
from app.blueprints.example.services import do_something

from app.blueprints.mongo.api_token_auth.helpers import get_user_from_request_headers
from app.blueprints.mongo.api_token_auth.token_verification import verify_token

from app.blueprints.example import bp

@bp.route("/feature", methods=["GET"])
def get_feature():
    # TODO: implement
    return jsonify({"status": "ok"})

@bp.route("/feature", methods=["POST"])
def create_feature():
    data = request.get_json() or {}

    # Delegate to service layer
    result = do_something(data)

    return jsonify({"result": result})

@bp.route('/auth-protected-feature', methods=["GET"])
@verify_token
def get_auth_protected_feature():
    time.sleep(1)
    user = get_user_from_request_headers(request.headers)
    if not user:
        return jsonify({"success": False, "message": "Not authorized"}), 401
    return jsonify({'success': True, 'message': 'Authorized', 'settings': user.settings}), 200

@bp.route('/auth-protected-feature', methods=["POST"])
@verify_token
def post_auth_protected_feature():
    user = get_user_from_request_headers(request.headers)
    user.settings['sound'] = request.form.get('sound')
    user.settings['volume'] = request.form.get('volume')
    user.save()
    return jsonify({'success': True, 'message': 'Authorized'}), 200