from app.blueprints.mongo.api_token_auth.helpers import decode_jwt
from flask import jsonify, request
import jwt
from functools import wraps

# decorator
def verify_token(func):

    @wraps(func)
    def inner(*args, **kwargs):
        from app.blueprints.mongo.api_token_auth.models import User

        encoded_token = request.headers.get('Authorization')
        if not encoded_token or encoded_token == "Bearer undefined":
            return jsonify({'error': 'User did not pass token in request'}), 401
        encoded_token = encoded_token.split(' ')[1]

        try:
            decoded = decode_jwt(encoded_token)
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({'error': 'Signature verification failed'}), 401

        if decoded:
            user = User.objects.get(email=decoded['email'])
        else:
            return jsonify({'error': 'User is not logged in.'}), 401

        # if user and decoded['code'] == user.jwt_code:
        if user: # we're just going to allow all sessions to exist simultaneously
            return func(*args, **kwargs)

        return jsonify({'error': 'User is not logged in.'}), 401

    return inner
