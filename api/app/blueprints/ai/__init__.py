from flask import Blueprint

bp = Blueprint(
    'ai',
    __name__,
    template_folder='templates',
    url_prefix='/ai'
)

# from app.blueprints.ai import routes