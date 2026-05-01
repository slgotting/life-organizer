from wtforms import Form, BooleanField, StringField, validators

class RegistrationForm(Form):
    email        = StringField('Email Address', [validators.Email(message="Invalid email address")])
    password     = StringField('Password', [validators.Length(min=8, message="Password must be at least 8 characters long"), ])

class LoginForm(Form):
    email        = StringField('Email Address', [validators.Email(message="Invalid email address")])
    password     = StringField('Password')