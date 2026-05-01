import sqlalchemy
from werkzeug.security import generate_password_hash
from flask import jsonify, request, current_app
from app.blueprints.sql.api_token_auth import bp
from app.blueprints.sql.api_token_auth.forms import RegistrationForm
from app.blueprints.sql.api_token_auth.sql_models import User
from app.blueprints.sql.api_token_auth.helpers import encode_jwt
from app import sql_db as db


@bp.route('/sign_up', methods=["POST"])
def sign_up():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            if not request.form.get('password') == request.form.get('confirm-password'):
                return jsonify({'success': False, 'message': 'Passwords must match', 'errors': ['Passwords must match']}), 400

            user = User(
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            user.generate_and_save_jwt_code()
            jwt = user.get_jwt()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Email is already taken.', 'errors': ['Email is already taken.']}), 409
        except Exception as e:
            current_app.logger.exception('exception')
            return jsonify({'success': False, 'message': 'Unknown', 'errors': ['Unknown error. The administrators have been notified.']}), 409

        return jsonify({'success': True, 'message': 'Signed up successfully', 'jwt': jwt}), 201

    return jsonify({'success': False, 'message': 'There was an issue trying to register the user.', 'errors': form.errors}), 409