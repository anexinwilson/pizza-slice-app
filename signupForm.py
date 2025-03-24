from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms import validators

class SignupForm(FlaskForm):
    email = StringField("Email:", [
        validators.InputRequired("Email is required") 
    ])
    password = PasswordField("Password:", [
        validators.InputRequired("Password is required"),  
        validators.Length(min=6, message="Password must be at least 6 characters")  
    ])
    confirm_password = PasswordField("Confirm Password:", [
        validators.InputRequired("Please confirm your password")  
    ])
    role = RadioField("Role:", choices=[
        ('s', 'Staff'), ('c', 'Customer')
    ], validators=[
        validators.InputRequired("Please select a role")  
    ])
    submit = SubmitField("Create Account")
