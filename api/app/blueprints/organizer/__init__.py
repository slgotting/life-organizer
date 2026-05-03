from flask import Blueprint

bp = Blueprint('organizer', __name__, url_prefix='/organizer')

from app.blueprints.organizer import routes
