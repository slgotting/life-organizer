from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from app.blueprints.sql.api_token_auth import bp
from app.blueprints.sql.api_token_auth.forms import LoginForm
from app.blueprints.sql.api_token_auth.sql_models import User
from app.blueprints.sql.api_token_auth.helpers import encode_jwt

from app import sql_db as db

@bp.route('/sign_in', methods=["POST"])
def sign_in():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one()
        except:
            return jsonify({'success': False, 'errors': ['Incorrect email or password.']}), 409
        password = request.form.get('password')
        if not check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'errors': ['Incorrect email or password.']}), 409
        user.generate_and_save_jwt_code()
        jwt = user.get_jwt()
        return jsonify({'success': True, 'message': 'Logged in successfully', 'jwt': jwt, 'errors': []}), 200

    return jsonify({'success': False, 'errors': ['Incorrect email or password.']}), 409