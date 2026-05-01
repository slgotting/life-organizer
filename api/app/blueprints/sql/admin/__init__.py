from flask import Blueprint

bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    url_prefix='/admin'
)

from app.blueprints.sql.admin import routes