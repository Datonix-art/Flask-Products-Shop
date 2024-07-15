from flask import redirect, render_template, url_for, Blueprint, flash
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from flask_babel import _
from store.core.forms import LogInForm, SignUpForm, ContactForm, EditUserForm
from store.core.models import UserModel, ContactModel
from store.shop.models import ProductModel

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
@core.route('/home')
def base():
    products = ProductModel.query.order_by(ProductModel.id.desc()).limit(4)
    return render_template('base.html', products=products)

@core.route('/contacts', methods=["GET", "POST"])
@login_required
def contacts():
    contactform = ContactForm()
    if contactform.validate_on_submit():
        try:  
            data = ContactModel(name=contactform.name.data, email=contactform.email.data, phoneNumber = contactform.phoneNumber.data, message = contactform.message.data) # type: ignore
            data.create()
            flash(_('Succesfully sent message!'), 'success')
            return redirect(url_for('core.base'))
        except IntegrityError as err:
            print(err._message())
    return render_template('base.html', form=contactform)

@core.route('/signup', methods=["GET", "POST"])
def signup():
    signupform = SignUpForm()
    if signupform.validate_on_submit():
        exisiting_account = UserModel.query.filter(signupform.email.data == UserModel.email).first() #type:ignore
        if not exisiting_account:
            data = UserModel(firstName = signupform.name.data, lastName=None, email = signupform.email.data, address=None, password = signupform.password.data) #type: ignore
            data.create()
            flash(_('Succesfull sign up. Please Login'), 'success')
            return redirect(url_for('core.login'))
        else:
            flash(_('Account with this email already exists. Please sign up with other one'), 'danger')
    return render_template('base.html', form=signupform)

@core.route('/login', methods=["GET", "POST"])
def login():
    loginform = LogInForm()
    if loginform.validate_on_submit():
        user = UserModel.query.filter(loginform.email.data == UserModel.email).first() #type: ignore
        if user and user.check_password(loginform.password.data):
            login_user(user)
            flash(_('succesfull login!'), 'success')
            return redirect(url_for('core.base'))
        else:
            flash(_('Email or password is incorrect. Log in again'), 'danger')
    return render_template('base.html', form=loginform)

@core.route('/logout', methods=["GET", "POST"]) # type: ignore
@login_required
def logout():
    logout_user()
    flash(_('Logged out succesfully'), 'success')
    return redirect(url_for('core.base'))

@core.route('/about')
def about():
    return render_template('base.html')

@core.route('/account/profile', methods=["GET", "POST"])
@login_required
def profile():
    form = EditUserForm()
    form.firstName.render_kw = {'placeholder': current_user.firstName}
    form.lastName.render_kw = {'placeholder': current_user.lastName if current_user.lastName else '(Undefined)'}
    form.email.render_kw = {'placeholder': current_user.email}
    form.address.render_kw = {'placeholder': current_user.address if current_user.address else '(Undefined)'}

    if form.validate_on_submit():
        existing_account = UserModel.query.filter(UserModel.email == form.email.data).first() # type: ignore

        if not existing_account or existing_account.id == current_user.id:
            current_user.firstName = form.firstName.data if form.firstName.data else current_user.firstName
            current_user.lastName = form.lastName.data if form.lastName.data else current_user.lastName
            current_user.email = form.email.data if form.email.data else current_user.email
            current_user.address = form.address.data if form.address.data else current_user.address

            if form.password.data and current_user.check_password(form.password.data):
                if form.newPassword.data:
                    current_user.password = generate_password_hash(form.newPassword.data)
         
          
            current_user.save()
            flash(_('Saved changes succesfully'), 'success')
            return redirect(url_for('core.profile'))
        else:
            flash(_('Account already exists with this email'), 'danger')
    return render_template('base.html', form=form)