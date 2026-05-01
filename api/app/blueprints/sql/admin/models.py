from sqlalchemy import Column, String, Integer
from flask_login import UserMixin
from app import sql_db as db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False)
    password_hash = Column(String, nullable=False)