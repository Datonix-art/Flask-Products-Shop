import os
from dotenv import load_dotenv

load_dotenv()

db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_dir, os.getenv('SQLALCHEMY_DATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    FLASK_ADMIN_SWATCH = 'yeti'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')