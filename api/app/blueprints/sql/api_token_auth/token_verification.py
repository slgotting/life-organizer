from app.blueprints.sql.api_token_auth.helpers import decode_jwt
from app.blueprints.sql.api_token_auth.sql_models import User
from flask import jsonify, request
import jwt
from slg_utilities.helpers import prnt
from functools import wraps
from app import sql_db as db

# decorator
def verify_token(func):

    @wraps(func)
    def inner(*args, **kwargs):
        encoded_token = request.headers.get('Authorization')
        if not encoded_token:
            return jsonify({'success': False, 'message': 'User did not pass token in request'}), 401
        encoded_token = encoded_token.split(' ')[1]

        try:
            decoded = decode_jwt(encoded_token)
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({'success': False, 'message': 'Signature verification failed'}), 401

        user = db.session.execute(db.select(User).filter_by(email=decoded.get('email'))).scalar_one()

        if user and decoded['code'] == user.jwt_code:
            return func(*args, **kwargs)

        return jsonify({'success': False, 'message': 'User is not logged in.'}), 401

    return inner
