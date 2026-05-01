from flask import Blueprint

bp = Blueprint(
    'example',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/example'
)

from app.blueprints.example import routes