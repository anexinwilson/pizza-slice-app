from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms import validators
from wtforms.validators import Email

class SignupForm(FlaskForm):
    email = StringField("Email", [
        validators.InputRequired("Email is required"), Email()
    ], render_kw={"placeholder": "Enter email"})
    password = PasswordField("Password", [
        validators.InputRequired("Password is required"),  
        validators.Length(min=6, message="Password must be at least 6 characters")  
    ], render_kw={"placeholder": "Create password"})
    confirm_password = PasswordField("Confirm Password", [
        validators.InputRequired("Please confirm your password")  
    ], render_kw={"placeholder": "Confirm password"})
    role = RadioField("Role", choices=[
        ('s', 'Staff'), ('c', 'Customer')
    ], validators=[
        validators.InputRequired("Please select a role")  
    ])
    submit = SubmitField("Create Account")
