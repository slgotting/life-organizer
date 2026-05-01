from flask import request, current_app, render_template
from app.blueprints.mongo.api_token_auth import bp
from app.blueprints.mongo.api_token_auth.models import User
from app.blueprints.mongo.api_token_auth.forms import ResetPasswordForm
from app.blueprints.mongo.api_token_auth.helpers import get_user_by_email, get_reset_password_url
from app.blueprints.email.email import send_email


@bp.route('/forgot-password', methods=["POST"])
def forgot_password():
    try:
        user = get_user_by_email(request.form['email'])
        if user:
            token = user.get_email_token()
            send_email(
                'Reset Password',
                [user.email],
                html_body=render_template(
                    'email/reset_password.html',
                    url=get_reset_password_url(token),
                    user=user
                )
            )
            return {'success': True}, 200
        return {'error': 'User not found'}, 404
    except:
        current_app.logger.exception('An unknown error occurred')
        return {'error': 'An unknown error occurred. Please bear with us as we look into the issue.'}, 500

@bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    success_obj = User.verify_email_token(token)
    if success_obj['success']:
        user = success_obj['user']
    else:
        return {'error': success_obj['message']}, 400

    form = ResetPasswordForm(request.form)

    if form.validate():
        password_set = user.set_password(form.data['password'])
        if password_set:
            user.generate_and_save_jwt_code()
            jwt = user.get_jwt()
            user.blacklist_token(token)
            return {'success': 'Password reset successfully!', 'jwt': jwt, 'user': user.email}, 200
        else:
            return {'error': 'Unknown error. Please try again.'}, 500
    else:
        errors = []
        for error_list in form.errors.values():
            errors += error_list
        errors = [f'- {err}' for err in errors]
        return {'error': "\n\n".join(errors)}, 400
