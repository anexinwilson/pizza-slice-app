from flask import Flask, render_template, redirect, url_for, session
import os
from dotenv import load_dotenv
import auth

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.secret_key = os.getenv('SECRET_KEY')

auth.auth_routes(app)

@app.route('/')
def home():
    if 'signin' not in session:
        return redirect(url_for('signin'))
    return render_template('home.html', email=session['user']['email'], role=session['role'])


if __name__ == '__main__':
    app.run(port = int(os.getenv('FLASK_RUN_PORT')), host = os.getenv('FLASK_RUN_HOST'))