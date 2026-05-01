import mongoengine
import pymongo
from werkzeug.security import generate_password_hash
from flask import request, current_app
from app.blueprints.mongo.api_token_auth import bp
from app.blueprints.mongo.api_token_auth.forms import RegistrationForm
from app.blueprints.mongo.api_token_auth.models import User
from app.blueprints.mongo.api_token_auth.helpers import encode_jwt


@bp.route('/sign_up', methods=["POST"])
def sign_up():
    print(f'\nrequest.form:\n {request.form}\n', flush=True)  # print flush variable snippet
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            if not request.form.get('password') == request.form.get('confirm-password'):
                return {'error': 'Passwords must match', 'errors': ['Passwords must match']}, 400
            user = User(
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
            )
            user.generate_and_save_jwt_code()
            jwt = user.get_jwt()
            user.save()
        except pymongo.errors.DuplicateKeyError:
            return {'error': 'Email is already taken.', 'errors': ['Email is already taken.']}, 409
        except mongoengine.errors.NotUniqueError:
            return {'error': 'Email is already taken.', 'errors': ['Email is already taken.']}, 409
        except Exception as e:
            current_app.logger.exception('exception')
            return {'error': 'Unknown error. Administrators have been notified', 'errors': ['Unknown error. The administrators have been notified.']}, 500

        return {'success': 'Signed up successfully', 'jwt': jwt, 'user': user.email}, 201

    return {'error': 'There was an issue trying to register the user.', 'errors': form.errors}, 400
