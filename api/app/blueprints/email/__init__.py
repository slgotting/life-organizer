from flask import Blueprint

bp = Blueprint(
    'email',
    __name__,
    template_folder='templates',
    url_prefix='/email'
)

# from app.blueprints.email import routes