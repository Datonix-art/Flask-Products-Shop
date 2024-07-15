import os
from dotenv import load_dotenv

load_dotenv()

db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_dir, os.getenv('SQLALCHEMY_DATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    FLASK_ADMIN_SWATCH = 'yeti'
