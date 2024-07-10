import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), os.getenv('SQLALCHEMY_DATABASE_URI'))
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') 
  BABEL_DEFAULT_LOCALE = 'en'
  BABEL_TRANSLATION_DIRECTORIES = os.path.join(os.getcwd(), "translations")