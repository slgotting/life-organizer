from app import sql_db as db
import jwt
from flask import current_app
import random
import string
from slg_utilities.helpers import prnt

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
    from app.blueprints.sql.api_token_auth.sql_models import User
    jwt = headers.get('Authorization').split(' ')[1]
    decoded = decode_jwt(jwt)
    if not decoded:
        return None
    user = db.session.execute(db.select(User).filter_by(email=decoded.get('email'))).scalar_one()
    return user

def get_user_by_id(id):
    from app.blueprints.sql.api_token_auth.sql_models import User
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    return user