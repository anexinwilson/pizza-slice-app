# app.py is  main file of the Pizza Slice Flask app.
# It sets the Flask app, loads environment variables, configures app settings,
# and registers route blueprints from `auth.py` and `pizza.py`.

# Key responsibilities:
                    #  - Loads environment variables from .flaskenv using load_dotenv().
                    #  - Loads app settings (e.g. port, debug, etc.) from settings.py.
                    #  - Sets the secret key used for session management.
                    #  - Registers route functions by calling auth_routes(app) and pizza_routes(app).
                    #  - Starts the web server if this file is run directly .

from flask import Flask
from dotenv import load_dotenv
from auth import auth_routes
from pizza import pizza_routes
from models import db
from flask_cors import CORS
from flask_wtf import CSRFProtect
import os

load_dotenv(override=True) # Load variables from .flaskenv file

app = Flask(__name__)

app.config.from_pyfile('settings.py') # Load config from settings.py
app.config['SECRE_KEY']=os.getenv('SECRET_KEY') # Set secret key from .env
# Create the database
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLALCHEMY_DATABASE_URI') # path for the SQLite database

# Initialise the database
db.init_app(app)

# initialise CORS
# used to protect HTML forms from unnecessary data inputs from the browser
CORS(app)
CSRFProtect(app)

# registers routes for auth like sign in ,sign out and signup by
#  importing the auth_route function from auth.py
app.register_blueprint(auth_routes)
app.register_blueprint(pizza_routes)

with app.app_context(): # Only run when app.py is executed
    db.create_all()
    print('Database created.')
    app.run(port=os.getenv('FLASK_RUN_PORT'), host=os.getenv('FLASK_RUN_HOST'), debug=True) # Run on port and host from .flaskenv
