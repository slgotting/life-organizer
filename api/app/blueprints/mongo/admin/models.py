import mongoengine as me
from flask_login import UserMixin


class Admin(UserMixin, me.Document):
    meta = {'strict': False}
    username = me.StringField(min_length=3, max_length=16)
    password_hash = me.StringField(required=True)