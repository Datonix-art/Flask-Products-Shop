from flask import Flask, redirect, render_template, request, session, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_babel import Babel, _, lazy_gettext
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from flask_mail import Mail
from store.config import Config
from dotenv import load_dotenv
import os
import stripe

load_dotenv()
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
mail = Mail()
admin = Admin(name='', template_mode='bootstrap4')

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.app_context().push()
 
    CORS(app)
    
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'core_bp.signup'
    login_manager.login_message = lazy_gettext('Please log in to access this page.')
    login_manager.login_message_category = 'danger'

    app.config.from_object(Config)

    mail.init_app(app)

    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    db.init_app(app)

    from store.core.routes import core_bp
    from store.cart.routes import cart_bp
    from store.shop.routes import shop_bp
    from store.payments.routes import payment_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(payment_bp)

    from store.core.models import UserModel

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    @app.errorhandler(404)
    def is_error(error):
        return render_template('base.html', is_error=True), 404
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template('base.html', reason=error.description), 400

    def get_locale():
        return session.get('lang', 'en')

    babel.init_app(app, locale_selector=get_locale)

    @app.route('/setlang', methods=["POST"])
    def setlang():
        lang = request.form.get('lang', 'en')
        if lang in ['en', 'ka']:
            session['lang'] = lang
        return redirect(request.referrer or url_for('core.base'))
    
    @app.context_processor
    def inject_locale():
        return {'get_locale': get_locale}
    
    from store.Admin.views import AdminModelView
    with app.test_request_context():
        admin.init_app(app, index_view=AdminModelView(name=lazy_gettext('Home'), template='admin/admin.html', url='/admin_panel'))
     
    return app
