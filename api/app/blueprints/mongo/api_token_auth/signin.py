import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from app.blueprints.mongo.api_token_auth import bp
from app.blueprints.mongo.api_token_auth.forms import LoginForm
from app.blueprints.mongo.api_token_auth.models import User
from app.blueprints.mongo.api_token_auth.helpers import encode_jwt


@bp.route('/sign_in', methods=["POST"])
def sign_in():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            return {'error': 'Incorrect email or password.'}, 401
        password = request.form.get('password')
        if not check_password_hash(user.password_hash, password):
            return {'error': 'Incorrect email or password.'}, 401
        user.generate_and_save_jwt_code()
        jwt = user.get_jwt()
        return {'success': 'Logged in successfully', 'jwt': jwt, 'user': user.email}, 200
    return {'error': 'Incorrect email or password.'}, 401