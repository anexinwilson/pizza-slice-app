from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

class SigninForm(FlaskForm):
    email = StringField("Email:", [
        validators.InputRequired("Email is required")
    ])
    password = PasswordField("Password:", [
        validators.InputRequired("Password is required")
    ])
    submit = SubmitField("Sign in")

