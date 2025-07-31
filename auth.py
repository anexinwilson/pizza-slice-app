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

auth_routes=Blueprint('auth', __name__)

# Function to load users from users.json and to be later used in other functions
def load_users():
    with open("data/users.json", "r") as file:
        return json.load(file)

# Function to save users to users.json and to be later used in other functions
def add_users(users):
    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4) # Add a indention of four spaces to json for better readability

# Check user credentials for sign in
def check_signin(email, password):
    users = load_users()  # Load all users json
    for person in users: # Loop through each user
        if person["email"] == email and person["password"] == password:
            return person # Return user if match found
    return None

# Function to define all auth routes

@auth_routes.route('/login', methods=['GET', 'POST'])  # This route handles login for both GET and POST methods
def login():
    form = SigninForm() # Create an instance of the sign-in form
    if form.validate_on_submit(): # If form is submitted and valid
        email = form.email.data # Get the email entered by user
        password = form.password.data # Get the email entered by user
        user = check_signin(email, password) # Check if the user exists
        if user: # # If user is found and credentials match
            session['signin'] = 'signed_in'  # Mark user as signed in
            session['user'] = user # Save entire user object to session
            session['role'] = user['role'] # Save user role
            return redirect(url_for('pizza.home')) # Redirect to home page after login
        else: # If credentials are wrong
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
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # If Password and confirm password fields do not match
        if form.password.data != form.confirm_password.data:  
            return render_template('signup.html', form=form, error="Passwords don't match")
        users = load_users() # Load existing users from JSON

        if any(user['email'] == email for user in users): # If Email already exists in the system
            return redirect(url_for('auth.create_account')) # redirect again to signup.html without creating the user

        # if Email is new and password matched — create new user and add to users.json
        new_user = { 
            "email": email,
            "password": password,
            "role": role
        }

        users.append(new_user) # Add new user to the user list
        add_users(users) # Save updated list back to users.json
        return redirect(url_for('auth.login')) # Redirect user to login page after account creation


@auth_routes.route('/logout')  # Route to logout
def logout():
    session.clear() # Clear all session data to log user out
    return redirect(url_for('auth.login'))  # Redirect user to login page