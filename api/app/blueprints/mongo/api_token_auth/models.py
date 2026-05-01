from flask import current_app
import time
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app.blueprints.mongo.api_token_auth.helpers import encode_jwt, random_string_generator
from app.blueprints.subscription.mixin_mongo import SubscriptionMixin
import mongoengine as me
from app import mongo_db as db
from typing import List

class BlacklistToken(me.Document):
    token = me.StringField()

    def __init__(self, **kwargs):
        super(BlacklistToken, self).__init__(**kwargs)

    def test(self):
        pass

class User(me.Document, SubscriptionMixin):
    meta = {'strict': False}
    first_name = me.StringField(required=False)
    last_name = me.StringField(required=False)
    email = me.EmailField(required=True, unique=True)
    email_verified = me.BooleanField(default=False)
    password_hash = me.StringField(required=True)

    jwt_code = me.StringField()

    notifications = me.DictField()

    # SETTINGS
    # WHENEVER ADD NEW SETTINGS MAKE SURE TO ADD IT TO THE SETTINGS PROPERTY
    # notify_interval = me.FloatField(default=6)
    # times_up_sound = me.StringField(default='Female 1')
    volume = me.FloatField(default=0.8)
    animation_volume = me.FloatField(default=0.4)

    member_since = me.DateTimeField(default=datetime.now)
    last_seen = me.DateTimeField(default=datetime.now)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        SubscriptionMixin.__init__(self)

    @property
    def settings(self):
        return {
            "volume": self.volume,
            "animation_volume": self.animation_volume,
        }

    def ping(self):
        self.last_seen = datetime.utcnow()
        self.save()

    def generate_jwt_code(self):
        return random_string_generator(10)

    def generate_and_save_jwt_code(self):
        self.jwt_code = self.generate_jwt_code()
        self.save()
        return self.jwt_code

    def get_jwt(self):
        return encode_jwt({'email': self.email, 'code': self.jwt_code})

    def revoke_token(self):
        self.jwt_code = ''
        self.save()
        return True

    def update_settings(self, web_form):
        self.volume = float(web_form.get('volume'))
        self.animation_volume = float(web_form.get('animationVolume'))
        self.save()

    def get_email_token(self, expires_in=600):
        return jwt.encode(
            {'id': str(self.id), 'exp': time.time() + expires_in},
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    def blacklist_token(self, token):
        BlacklistToken(token=token).save()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.save()
        return True

    @staticmethod
    def verify_email_token(token):
        token = token.strip('"')

        if BlacklistToken.objects(token=token).first():
            return {'success': False, 'message': 'Token has expired. Please request a new password reset.'}

        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'),
                                algorithms=[current_app.config.get('JWT_ALGORITHM', 'HS256')])
        except jwt.exceptions.ExpiredSignatureError:
            return {'success': False, 'message': 'Token has expired. Please request a new password reset.'}

        try:
            id = data['id']
        except:
            return {'success': False, 'message': 'Token is invalid.'}

        user = User.objects(id=id).first()

        if user:
            return {'success': True, 'user': user}

        return {'success': False, 'message': 'Token is invalid.'}


    def __str__(self):
        attributes = vars(self)
        attribute_str = "\n".join(f"{key}: {value}" for key, value in attributes.items())
        return attribute_str
