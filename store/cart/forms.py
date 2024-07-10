from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange
from wtforms import FieldList, FormField, IntegerField, SubmitField, HiddenField
from flask_babel import lazy_gettext

class CartItemForm(FlaskForm):
    new_amount = IntegerField('Amount', validators=[InputRequired(), NumberRange(min=1, max=100)])
    item_id = HiddenField('Item ID')  

class CartForm(FlaskForm):
    items = FieldList(FormField(CartItemForm), min_entries=1)
    update_cart = SubmitField(lazy_gettext('Update Cart'))
