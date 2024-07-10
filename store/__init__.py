import os

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__, template_folder='templates')
app.app_context().push()

from flask_cors import CORS

CORS(app)

from flask_babel import Babel, _, lazy_gettext

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'core.signup'
login_manager.login_message = lazy_gettext('Please log in to access this page.')
login_manager.login_message_category = 'danger'


from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), os.getenv('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] =  os.path.join(os.getcwd(), "translations")

db = SQLAlchemy(app)

from store.core.routes import core
from store.cart.routes import cart
from store.shop.routes import shop

app.register_blueprint(core)
app.register_blueprint(cart)
app.register_blueprint(shop)

from store.core.models import UserModel

@login_manager.user_loader
def load_user(user_id):
  return UserModel.query.get(int(user_id))

@app.errorhandler(404)
def is_error(error):
    return render_template('base.html', is_error=True), 404

def get_locale():
  return session.get('lang', 'en')

babel = Babel(app, locale_selector = get_locale)

@app.route('/setlang', methods=["POST"])
def setlang():
  lang = request.form.get('lang', 'en')
  if lang in ['en', 'ka']:
    session['lang'] = lang
  return redirect(request.referrer or url_for('core.base'))

@app.context_processor 
def inject_locale():
  return {'get_locale': get_locale}
