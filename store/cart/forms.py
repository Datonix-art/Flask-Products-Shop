from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange
from wtforms import IntegerField, SubmitField

class CartForm(FlaskForm):
    new_amount = IntegerField('Amount', validators=[InputRequired(), NumberRange(min=1, max=100)])
    update_cart = SubmitField('Update Cart')
