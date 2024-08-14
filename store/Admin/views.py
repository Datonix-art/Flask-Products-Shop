from flask import abort, current_app, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_login import current_user
from flask_babel import lazy_gettext, _
from markupsafe import Markup
from store import admin, db
import PIL
import os

# https://github.com/pallets-eco/flask-admin/blob/master/examples/forms-files-images/app.py#L144-L162
# admin user: email = '', password = '', url='/admin_panel/'

class AdminModelView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.email == 'ProductShopAdmin123@gmail.com':
            return True
        else:
            abort(404)     

media_path = os.path.join(current_app.root_path, 'static', 'images', 'product_images')

try:
    os.makedirs(media_path)
except OSError:
    pass

class ImageView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        
        return Markup('<img src="%s" width="50">' % url_for('static', filename='images/product_images/' + model.image))
    
    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'image' : ImageUploadField('Image', base_path=media_path)
    }

from store.core.models import UserModel, ContactModel
from store.shop.models import ProductModel, OrderModel

class UserAdminModelView(ModelView):
    column_list = ('id', 'firstName', 'lastName', 'email', 'address')
    column_searchable_list = ('firstName', 'lastName')
    column_filters = ('email', 'firstName')
    page_size: 10
    can_view_details = True
    can_export = True
    can_create = True
    can_delete = True

class ContactAdminModelView(ModelView):
    column_list = ('id', 'name', 'email', 'phoneNumber', 'message')
    column_searchable_list = ('email', )
    column_filters = ('email', 'phoneNumber')
    page_size: 10
    can_view_details = True
    can_edit = False
    can_delete = False
    can_create = False

class ProductAdminModelView(ImageView):
    column_list =  ('id', 'image', 'category_id', 'name', 'slug', 'description', 'price', 'amount')
    column_searchable_list = ('name', 'price')
    column_filters = ('category_id', 'name')
    form_columns = ['image', 'category_id', 'name', 'slug', 'description', 'price']
    page_size: 10
    can_view_details = True
    can_edit = True
    can_create = True
    can_delete = True

    def on_model_delete(self, model):
        if model.image:
            try: 
                image_path = os.path.join(media_path, model.image)
                os.remove(image_path)
            except:
                pass

class OrderAdminModelView(ModelView):
    column_list = ('user_id', 'first_name', 'company_name', 'street_address', 'apartment', 'town_city', 'number', 'email', 'total_price', 'created_at')
    column_searchable_list = ('user_id', 'email', 'number')
    column_filters = ('first_name', 'company_name', 'street_address', 'town_city')
    page_size: 10
    can_delete = True
    can_view_details = True
    can_export = True
    can_create = False


def setup_admin_views():
    with current_app.test_request_context():
        admin.add_view(UserAdminModelView(UserModel, db.session, name=lazy_gettext('User Panel'), endpoint='user_panel'))
        admin.add_view(ContactAdminModelView(ContactModel, db.session, name=lazy_gettext('Contact Panel'), endpoint='contact_panel'))
        admin.add_view(ProductAdminModelView(ProductModel, db.session, name=lazy_gettext('Product Panel'), endpoint='product_model'))
        admin.add_view(OrderAdminModelView(OrderModel, db.session, name=lazy_gettext('Order Panel'), endpoint='order_model'))

setup_admin_views()
