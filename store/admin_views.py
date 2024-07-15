from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from flask_admin import AdminIndexView

class AdminModelView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.email == 'ProductShopAdmin123@gmail.com':
            return True
        else:
            abort(404)     
    
