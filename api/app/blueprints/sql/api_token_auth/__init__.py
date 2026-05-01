from flask import Blueprint

bp = Blueprint(
    'api_token_auth',
    __name__,
    url_prefix="/auth",
)

from app.blueprints.sql.api_token_auth import signup, signin, routes
