# this is not used, here for reference, would typically be named just models.py
# but its interfering with file selection

import copy
from datetime import datetime
from sqlalchemy import Integer, Column, DateTime, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.blueprints.sql.api_token_auth.helpers import encode_jwt, random_string_generator
from app import sql_db as db

class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)

    def __init__(self, token=None):
        self.token = token

    def test(self):
        pass

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    password_hash = Column(String, nullable=False)
    jwt_code = Column(String)

    settings_id = Column(Integer, ForeignKey('user_settings.id'))
    notifications_id = Column(Integer, ForeignKey('user_notifications.id'))

    settings = relationship("UserSettings", uselist=False)
    notifications = relationship("UserNotifications", uselist=False)

    member_since = Column(DateTime, default=datetime.now)
    last_seen = Column(DateTime, default=datetime.now)

    groups = Column(JSON, default={})

    def __init__(self, email, password_hash, email_verified=False, jwt_code=None, notifications=None, settings=None, groups=None, **kwargs):
        self.email = email
        self.password_hash = password_hash
        self.email_verified = email_verified
        self.jwt_code = jwt_code
        self.notifications = notifications or UserNotifications()
        self.settings = settings or UserSettings()
        super().__init__(**kwargs)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def generate_jwt_code(self):
        return random_string_generator(10)

    def generate_and_save_jwt_code(self):
        self.jwt_code = self.generate_jwt_code()
        db.session.add(self)
        db.session.commit()
        return self.jwt_code

    def get_jwt(self):
        return encode_jwt({'email': self.email, 'code': self.jwt_code})

    def revoke_token(self):
        self.jwt_code = ''
        db.session.add(self)
        db.session.commit()
        return True

    def update_groups_key(self, key, value):
        self.groups = copy.deepcopy(self.groups)
        self.groups[key] = value
        db.session.add(self)
        db.session.commit()

    def update_groups(self, new_groups_object):
        self.groups = new_groups_object
        db.session.add(self)
        db.session.commit()
        assert self.groups == new_groups_object

    def get_first_member_id_available(self, group_name):
        ids = list(map(lambda el: el['id'], self.groups[group_name]['members']))
        return max(ids) + 1 if ids else 1

    def __str__(self):
        attributes = vars(self)
        attribute_str = "\n".join(f"{key}: {value}" for key, value in attributes.items())
        return attribute_str

class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    setting1 = Column(String)
    setting2 = Column(Integer)

    user = relationship("User", back_populates="settings")

class UserNotifications(db.Model):
    __tablename__ = 'user_notifications'

    id = Column(Integer, primary_key=True)
    notification1 = Column(String)
    notification2 = Column(Integer)

    user = relationship("User", back_populates="notifications")