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
import os
from dotenv import load_dotenv
from auth import auth_routes
from pizza import pizza_routes

load_dotenv() # Load variables from .flaskenv file

app = Flask(__name__)
app.config.from_pyfile('settings.py') # Load config from settings.py
app.secret_key = os.getenv('SECRET_KEY') # Set secret key from .env

# registers routes for auth like sign in ,sign out and signup by
#  importing the auth_route function from auth.py
auth_routes(app)  

# Registers routes for pizza ordering  like create, edit,
# update, delete, and view orders by importing the pizza_routes function from pizza.py
pizza_routes(app)

if __name__ == '__main__': # Only run when app.py is executed
    app.run(port=int(os.getenv('FLASK_RUN_PORT')), host=os.getenv('FLASK_RUN_HOST')) # Run on port and host from .flaskenv
