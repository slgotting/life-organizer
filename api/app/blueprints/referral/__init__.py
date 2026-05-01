from flask import Blueprint

bp = Blueprint(
    'referral',
    __name__,
    template_folder='templates',
    url_prefix='/referral'
)

from app.blueprints.referral import routes