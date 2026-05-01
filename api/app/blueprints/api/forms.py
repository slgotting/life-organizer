from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
# from app.blueprints.api.models import ReferringUser

# class RegistrationForm(FlaskForm):
#     phone_number = StringField('Phone Number', validators=[DataRequired()])
#     def validate_username(self, phone_number):
#         user = ReferringUser.objects(phone_number=phone_number).first()
#         if user is not None:
#             raise ValidationError(('This phone number is already in the system.'))

class MemberForm(FlaskForm):
    class Meta:
        csrf = False

    group_name = StringField('Group Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=50, message="Name must be less than 50 characters")])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')])