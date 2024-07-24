from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask import abort
from flask_login import current_user
from store import admin, db
import os

class AdminModelView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.email == 'ProductShopAdmin123@gmail.com':
            return True
        else:
            abort(404)     

media_path = os.path.join(os.path.dirname(__file__), 'static/images/product_images')

try:
    os.mkdir(media_path)
except OSError:
    pass

from store.core.models import UserModel, ContactModel
from store.shop.models import ProductModel, OrderModel

class UserAdminModelView(ModelView):
    column_list = ('id', 'firstName', 'lastName', 'email', 'address')
    column_searchable_list = ('firstName', 'lastName')
    column_filters = ('email', 'firstName')
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True

class ContactAdminModelView(ModelView):
    column_list = ('id', 'name', 'email', 'phoneNumber', 'message')
    column_searchable_list = ('email', )
    column_filters = ('email', 'phoneNumber')
    can_view_details = True
    can_edit = False
    can_delete = False
    can_create = False

class ProductAdminModelView(ModelView):
    column_list =  ('id', 'image', 'category_id', 'name', 'slug', 'description', 'price', 'amount')
    column_searchable_list = ('name', 'price')
    column_filters = ('category_id', 'name')
    form_create_rules = ('image', 'category_id', 'name', 'slug', 'description', 'price')
    can_view_details = True
    can_edit = True
    can_create = True

    form_extra_fields = {
      'image' : ImageUploadField(base_path=media_path)
    }
  

    def on_model_delete(self, model):
        if model.image:
            try: 
                image_path = os.path.join(media_path, model.image)
                os.remove(image_path)
            except:
                pass


def setup_admin_views():
    admin.add_view(UserAdminModelView(UserModel, db.session, name='User Panel', endpoint='user_panel', category='User'))
    admin.add_view(ContactAdminModelView(ContactModel, db.session, name='Contact Panel', endpoint='contact_panel', category='User'))
    admin.add_view(ProductAdminModelView(ProductModel, db.session, name='Product Model', endpoint='product_model', category='Product'))


setup_admin_views()