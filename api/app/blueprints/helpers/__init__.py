from flask import Blueprint

bp = Blueprint(
    'helpers',
    __name__,
    template_folder='templates',
    url_prefix='/helpers'
)

# from app.blueprints.helpers import routes