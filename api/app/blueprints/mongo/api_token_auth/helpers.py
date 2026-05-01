import jwt
from flask import current_app
import random
import string

def encode_jwt(data):
    encoded = jwt.encode(
        data,
        current_app.config['SECRET_KEY'],
        algorithm=current_app.config.get('JWT_ALGORITHM', 'HS256'),
    )
    return encoded

def decode_jwt(jwt_):
    if not jwt_ or jwt_ == 'null':
        return
    jwt_ = jwt_.strip('"')
    try:
        return jwt.decode(
            jwt_,
            current_app.config['SECRET_KEY'],
            algorithms=[current_app.config.get('JWT_ALGORITHM', 'HS256')],
        )
    except jwt.exceptions.InvalidSignatureError:
        return 'Invalid Signature'

def random_string_generator(str_size):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_size))

def get_user_from_request_headers(headers):
    from app.blueprints.mongo.api_token_auth.models import User
    jwt = headers.get('Authorization').split(' ')[1]
    decoded = decode_jwt(jwt)
    if not decoded:
        return None
    user = User.objects.get(email=decoded.get('email'))
    return user

def get_user_by_id(id):
    from app.blueprints.mongo.api_token_auth.models import User
    user = User.objects.get(id=id)
    return user

def get_user_by_email(email):
    from app.blueprints.mongo.api_token_auth.models import User
    user = User.objects.get(email=email)
    return user

def get_reset_password_url(token):
    client_uri = current_app.config.get('CLIENT_URI')
    return f'{client_uri}/reset-password?token={token}'

def get_account_deletion_url(token):
    client_uri = current_app.config.get('CLIENT_URI')
    return f'{client_uri}/confirm_account_deletion?token={token}'