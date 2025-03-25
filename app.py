from flask import Flask
import os
from dotenv import load_dotenv
from auth import auth_routes
from pizza import pizza_routes

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.secret_key = os.getenv('SECRET_KEY')

auth_routes(app)
pizza_routes(app)

if __name__ == '__main__':
    app.run(port=int(os.getenv('FLASK_RUN_PORT')), host=os.getenv('FLASK_RUN_HOST'))
