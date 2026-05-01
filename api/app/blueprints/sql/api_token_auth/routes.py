import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from app.blueprints.sql.api_token_auth import bp
from app.blueprints.sql.api_token_auth.forms import LoginForm
from app.blueprints.sql.api_token_auth.sql_models import User
from app.blueprints.sql.api_token_auth.helpers import decode_jwt, encode_jwt, get_user_from_request_headers
from app.blueprints.sql.api_token_auth.token_verification import verify_token
from app import sql_db as db

from slg_utilities.helpers import prnt

# @bp.route('/verify_token_', methods=["POST"])
# def verify_token_route():

#     print(request.form, flush=True)
#     form = LoginForm(request.form)
#     print(form.data)
#     if request.method == 'POST' and form.validate():
#         email = request.form.get('email')
#         user = User.objects.get(email=email)
#         password = request.form.get('password')
#         if not check_password_hash(user.password_hash, password):
#             return jsonify({'success': False, 'message': 'Incorrect email or password.'}), 200
#         user.generate_jwt_code()
#         jwt = user.get_jwt()
#         return jsonify({'success': True, 'message': 'Logged in successfully', 'jwt': jwt}), 200

#     return jsonify({'success': False, 'message': 'Incorrect email or password.'}), 200

@verify_token
@bp.route('/authorize', methods=["POST"])
def authorize():
    jwt = request.headers.get('Authorization').split(' ')[1]
    page = request.form.get('page')
    decoded = decode_jwt(jwt)
    if not decoded:
        return jsonify({"success": False, "message": "Not authorized"}), 401

    user = db.session.execute(db.select(User).filter_by(email=decoded.get('email'))).scalar_one()
    if user:
        return jsonify({'success': True, 'message': 'Authorized'}), 200

    return jsonify({"success": False, "message": "Not authorized"}), 401

@bp.route('/test_data', methods=["GET"])
@verify_token
def test_data():
    time.sleep(1)
    user = get_user_from_request_headers(request.headers)
    if not user:
        return jsonify({"success": False, "message": "Not authorized"}), 401
    return jsonify({'success': True, 'message': 'Authorized', 'settings': user.settings}), 200

@bp.route('/test_post_data', methods=["POST"])
@verify_token
def test_post_data():
    user = get_user_from_request_headers(request.headers)
    user.settings['sound'] = request.form.get('sound')
    user.settings['volume'] = request.form.get('volume')
    user.save()
    return jsonify({'success': True, 'message': 'Authorized'}), 200