from flask import Blueprint

bp = Blueprint(
    'api_token_auth',
    __name__,
    url_prefix="/auth",
)

from app.blueprints.mongo.api_token_auth import signup, signin, routes, reset_password, delete_account
