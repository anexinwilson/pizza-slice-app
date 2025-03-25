from flask import render_template, request, redirect, url_for, session
from signupForm import SignupForm  
from signinForm import SigninForm 
import json

def load_users():
    with open("data/users.json", "r") as file:
        return json.load(file)

def add_users(users):
    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4)

def check_signin(email, password):
    users = load_users()
    for person in users:
        if person["email"] == email and person["password"] == password:
            return person
    return None

def auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = SigninForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = check_signin(email, password)
            if user:
                session['signin'] = 'signed_in'
                session['user'] = user
                session['role'] = user['role']
                return redirect(url_for('home'))
            else:
                return render_template('signin.html', form=form, error="Invalid email or password")
        return render_template('signin.html', form=form)

    @app.route('/create', methods=['GET', 'POST'])
    def create_account():
        form = SignupForm()

        if request.method == 'GET':
            return render_template('signup.html', form=form)

        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            if form.password.data != form.confirm_password.data:  
                return render_template('signup.html', form=form, error="Passwords don't match")
            users = load_users()

            if any(user['email'] == email for user in users):
                return redirect(url_for('create_account'))

            new_user = {
                "email": email,
                "password": password,
                "role": role
            }

            users.append(new_user)
            add_users(users)
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))