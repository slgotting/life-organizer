from flask import Blueprint

bp = Blueprint(
    'error',
    __name__,
    template_folder='templates',
    url_prefix='/error'
)

from app.blueprints.error import test_routes