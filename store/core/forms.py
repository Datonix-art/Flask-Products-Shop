from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, IntegerField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, EqualTo
from flask_babel import lazy_gettext

class ContactForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[DataRequired(), Length(min=3, max=15)], render_kw={'placeholder': lazy_gettext('Your name')})
    email = EmailField(lazy_gettext('Email'), validators=[DataRequired()], render_kw={'placeholder': lazy_gettext('Your email')})
    phoneNumber = IntegerField(lazy_gettext('Phone'), validators=[DataRequired()], render_kw={'placeholder': lazy_gettext('Your phone'), 'type': 'tel'})
    message = TextAreaField(lazy_gettext('Message'), validators=[DataRequired(), Length(min=15, max=400)], render_kw={'placeholder': lazy_gettext('Your message')})
    submit = SubmitField(lazy_gettext('Send message'))

class SignUpForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[DataRequired(), Length(min=3, max=15)], render_kw={'placeholder': lazy_gettext('First name')})
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Length(min=1, max=320)], render_kw={'placeholder': lazy_gettext('Email')})
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), Length(min=8, max=40)], render_kw={'placeholder': lazy_gettext('Password')})
    createAcc = SubmitField(lazy_gettext('Create Account'))

class LogInForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(), Length(min=1, max=320)], render_kw={'placeholder': lazy_gettext('Email')})
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), Length(min=8, max=40)], render_kw={'placeholder': lazy_gettext('Password')})
    logIn = SubmitField(lazy_gettext('Log in'))

class EditUserForm(FlaskForm):
    firstName = StringField(lazy_gettext('First Name'), validators=[Optional(), Length(min=3, max=15)])
    lastName = StringField(lazy_gettext('Last Name'), validators=[Optional(), Length(min=5, max=20)], render_kw={'placeholder': lazy_gettext('Last Name')})
    email = StringField(lazy_gettext('Email'), validators=[Optional(), Length(min=1, max=320)])
    address = StringField(lazy_gettext('Address'), validators=[Optional(), Length(min=10, max=30)])
    password = PasswordField(lazy_gettext('Password Changes'), validators=[DataRequired(), Length(min=8, max=40)], render_kw={'placeholder': lazy_gettext('Current Password')})
    newPassword = PasswordField(lazy_gettext('New Password'), validators=[Optional(),  Length(min=8, max=40)], render_kw={'placeholder': lazy_gettext('New Password')})
    confirmNewPassword = PasswordField(lazy_gettext('Confirm New Password'), validators=[Optional(), EqualTo('newPassword')], render_kw={'placeholder': lazy_gettext('Confirm New Password')})
    save = SubmitField(lazy_gettext('Save Changes'))
