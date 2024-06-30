from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, SubmitField, StringField, EmailField
from wtforms.validators import InputRequired, Length, Optional
from flask_babel import lazy_gettext

class BuyingForm(FlaskForm):
  product_color = RadioField(lazy_gettext('Colours:'), choices=['', ''],validators=[InputRequired()])
  product_amount = IntegerField()
  Buy = SubmitField(lazy_gettext('Buy Now'))


class CheckoutForm(FlaskForm):
  first_name = StringField('First Name*', validators=[InputRequired(), Length(min=3, max=15)])
  company_name = StringField('Company Name', validators=[InputRequired(), Length(min=5, max=20)])
  street_address = StringField('Street address*', validators=[InputRequired(), Length(min=10, max=30)])
  apartment = StringField('Apartment, floor, etc. (optional)', validators=[Optional()])
  town_city = StringField('Town/City*', validators=[InputRequired()])
  number = IntegerField('Phone Number*', validators=[InputRequired()])
  email = EmailField('Email*', validators=[InputRequired()])
  place_order = SubmitField('Place Order')