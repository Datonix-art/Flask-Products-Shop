from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, EmailField
from wtforms.validators import InputRequired, Length, Optional
from flask_babel import lazy_gettext

class BuyingForm(FlaskForm):
  Buy = SubmitField(lazy_gettext('Buy Now'))


class CheckoutForm(FlaskForm):
  first_name = StringField(lazy_gettext('First Name*'), validators=[InputRequired(), Length(min=3, max=15)])
  company_name = StringField(lazy_gettext('Company Name'), validators=[InputRequired(), Length(min=5, max=20)])
  street_address = StringField(lazy_gettext('Street address*'), validators=[InputRequired(), Length(min=10, max=30)])
  apartment = StringField(lazy_gettext('Apartment, floor, etc. (optional)'), validators=[Optional()])
  town_city = StringField(lazy_gettext('Town/City*'), validators=[InputRequired()])
  number = IntegerField(lazy_gettext('Phone Number*'), validators=[InputRequired()])
  email = EmailField(lazy_gettext('Email*'), validators=[InputRequired()])
  place_order = SubmitField(lazy_gettext('Place Order'))