from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators

class SigninForm(FlaskForm):
    email = StringField("Email:", [
        validators.InputRequired("Email is required") 
    ], render_kw={"placeholder": "Enter email"})
    password = PasswordField("Password:", [
        validators.InputRequired("Password is required")  
    ], render_kw={"placeholder": "Enter password"})
    submit = SubmitField("Sign in")
