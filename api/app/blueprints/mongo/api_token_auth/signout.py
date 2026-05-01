from flask import jsonify, request
from app.blueprints.mongo.api_token_auth.helpers import decode_jwt
from app.blueprints.mongo.api_token_auth.models import User
from app.blueprints.mongo.api_token_auth import bp
from app.blueprints.mongo.api_token_auth.forms import RegistrationForm
from app.blueprints.mongo.api_token_auth.token_verification import verify_token



@bp.route('/sign_out', methods=["POST"])
@verify_token
def sign_out():
    decoded = decode_jwt(request.form.get('jwt'))
    user = User.objects.get(email=decoded['email'])
    if user:
        user.revoke_token()
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    else:
        return jsonify({'success': False, 'message': 'Something went wrong'})
