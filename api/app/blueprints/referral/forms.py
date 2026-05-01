from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.blueprints.referral.models import ReferringUser


class RegistrationForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    def validate_username(self, phone_number):
        user = ReferringUser.objects(phone_number=phone_number).first()
        if user is not None:
            raise ValidationError(('This phone number is already in the system.'))
