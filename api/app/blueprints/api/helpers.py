import jwt
from flask import current_app

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

def decode_jwt_no_signature_check(jwt_):
    if not jwt_ or jwt_ == 'null':
        return
    jwt_ = jwt_.strip('"')
    return jwt.decode( jwt_, verify=False )

def build_jwt_url(url, data):
    jwt = encode_jwt(data)
    return f'{url}?jwt={jwt}'
