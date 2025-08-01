# auth.py handles user authentication for the Pizza Slice web application.
# It defines routes for user login, account creation, and logout using Flask routes.
# WTForms is used to validate form inputs for both sign-in and sign-up forms.
# User data such as email, password, and role is stored in users.json.
# The purpose of this file is to manage who can access the app by checking user credentials and managing sessions.
# It ensures that only logged-in users can access protected pages like placing or viewing pizza orders.
# Sessions are used to keep users logged in and to store their role, which helps control what they can see or do.

from flask import render_template, request, redirect, url_for, session, Blueprint
from signupForm import SignupForm  
from signinForm import SigninForm 
import json
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_routes=Blueprint('auth', __name__)

# Function to load users from users.json and to be later used in other functions
def load_users():
    # Query from the database
    users = User.query.all()
    users_dict = [user.to_dict() for user in users] 
    return json.dumps(users_dict)

# Function to save users to users.json and to be later used in other functions
def add_users(user):
    # Add to the database
    db.session.add(user)
    db.session.commit()

# Check user credentials for sign in
def check_signin(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    if user.email == email and check_password_hash(user.password_hash, password):
        return user # Return user if match found

# define all auth routes
@auth_routes.route('/login', methods=['GET', 'POST'])  # This route handles login for both GET and POST methods
def login():
    form = SigninForm() # Create an instance of the sign-in form
    if form.validate_on_submit(): # If form is submitted and valid
        email = form.email.data # Get the email entered by user
        password = form.password.data # Get the email entered by user
        user = check_signin(email, password) # Check if the user exists
        if user: # # If user is found and credentials match
            session['signin'] = 'signed_in'  # Mark user as signed in
            session['user'] = user.email # Save entire user object to session
            session['role'] = user.role # Save user role
            # I noticed that the staff members and the customers are getting the same data when they are logged in
            # I have separated their data based on their separate roles
            # Redirect the staff member to the dashboard after login
            if user.role == 's':
                return render_template('admin.html', email=user.email)
            return redirect(url_for('pizza.home')) # Redirect customers to home page after login
        # If credentials are wrong
        return render_template('signin.html', form=form, error="Invalid email or password")
    return render_template('signin.html', form=form) # If GET request, show empty login form

# This route handles creation of a new user account
@auth_routes.route('/create', methods=['GET', 'POST'])
def create_account():
    form = SignupForm() # Create instance of signup form

    if request.method == 'GET': # If It's a GET request, show the registration form
        return render_template('signup.html', form=form) 

    elif request.method == 'POST': # If it's a POST request then form submitted is submitted
        # Retrieve form data directly from  the request 
        email = form.email.data
        password = form.password.data
        comfirm_password = form.confirm_password.data
        role = form.role.data

        # If Password and confirm password fields do not match
        if password != comfirm_password:  
            return render_template('signup.html', form=form, error="Passwords don't match")
        
        # Check if the user email already exists
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', form=form, error='Email already exists')

        # Hash user password before storage
        password_hash = generate_password_hash(password) 
        new_user = User(
            email=email,
            password_hash=password_hash,
            role=role
        )

        add_users(new_user) # Save updated list back to users.json
        return redirect(url_for('auth.login')) # Redirect user to login page after account creation

@auth_routes.route('/logout')  # Route to logout
def logout():
    session.clear() # Clear all session data to log user out
    return redirect(url_for('auth.login'))  # Redirect user to login page