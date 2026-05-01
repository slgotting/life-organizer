from flask import Blueprint

bp = Blueprint(
    'subscription',
    __name__,
    template_folder='templates',
    url_prefix='/subscription'
)


from app.blueprints.subscription import routes