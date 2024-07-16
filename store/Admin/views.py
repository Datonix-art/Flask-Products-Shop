from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort, redirect, url_for
from flask_admin import AdminIndexView
from store import admin, db
from store.core.models import ContactModel, UserModel

class AdminModelView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.email == 'ProductShopAdmin123@gmail.com':
            return True
        else:
            abort(404)     
    
class UserAdminModelView(ModelView):
    column_list = ('id', 'firstName', 'lastName', 'email', 'address')
    column_searchable_list = ('firstName', )
    column_filters = ('email', 'firstName')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == 'ProductShopAdmin123@gmail.com'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('core.login'))

def setup_admin_views():
    admin.add_view(UserAdminModelView(UserModel, db.session, name='User Panel', endpoint='user_panel', category='User'))

setup_admin_views()