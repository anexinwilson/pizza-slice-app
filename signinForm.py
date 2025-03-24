from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

class SigninForm(FlaskForm):
    email = StringField("Email:", [
        validators.InputRequired("Email is required")  # Use validators namespace explicitly
    ])
    password = PasswordField("Password:", [
        validators.InputRequired("Password is required")  # Use validators namespace explicitly
    ])
    submit = SubmitField("Sign in")
