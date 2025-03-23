from os import environ, getenv
from dotenv import load_dotenv


load_dotenv('./.flaskenv')
SECRET_KEY = getenv('SECRET_KEY')
