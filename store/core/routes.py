from flask import redirect, render_template, request, url_for, Blueprint, flash, current_app
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from flask_babel import _
from store.core.forms import LogInForm, RequestResetForm, ResetPasswordForm, SignUpForm, ContactForm, EditUserForm
from store.core.models import UserModel, ContactModel
from store.shop.models import ProductModel
from store import mail
from store.core.token import generate_token, confirm_token
from store.core.email import send_email

core_bp = Blueprint('core_bp', __name__, template_folder='templates')

@core_bp.route('/')
@core_bp.route('/home')
def base():
    products = ProductModel.query.order_by(ProductModel.id.desc()).limit(4)
    return render_template('base.html', products=products)

@core_bp.get('/search/<int:page_id>')
def search(page_id):
    search = request.args.get('search', '')
    search_results = ProductModel.query.filter(ProductModel.name.ilike(f'%{search}%')).paginate(per_page=4, page=page_id)
    return render_template('base.html', search_results=search_results)

@core_bp.route('/contacts', methods=["GET", "POST"])
@login_required
def contacts():
    contactform = ContactForm()
    if contactform.validate_on_submit():
        try:  
            data = ContactModel(
                name=contactform.name.data, 
                email=contactform.email.data, 
                phoneNumber=contactform.phoneNumber.data, 
                message=contactform.message.data
            )
            data.create()
            flash(_('Successfully sent message!'), 'success')
            return redirect(url_for('core_bp.base'))
        except IntegrityError as err:
            flash(_('An error occurred while sending your message.'), 'danger')
            current_app.logger.error(err)
    return render_template('base.html', form=contactform)

@core_bp.route('/signup', methods=["GET", "POST"])
def signup():
    signupform = SignUpForm()
    if signupform.validate_on_submit():
        existing_account = UserModel.query.filter_by(email=signupform.email.data).first()
        if not existing_account:
            user = UserModel(
                firstName=signupform.name.data, 
                lastName=None, 
                email=signupform.email.data, 
                address=None, 
                password=generate_password_hash(signupform.password.data)
            )
            user.create()
            email = user.email
            token = generate_token(email)
            verify_url = url_for('core_bp.verify_email', token=token, _external=True)
            html = render_template('verify_email/verify_email.html', verify_url=verify_url)
            subject = "Please confirm your email"
            send_email(email, subject, html)
            login_user(user)
            flash(_('A confirmation email has been sent via email.'), 'success')
            return redirect(url_for('core_bp.base'))
        else:
            flash(_('Account with this email already exists. Please sign up with another one'), 'danger')
    return render_template('base.html', form=signupform)

@core_bp.route('/login', methods=["GET", "POST"])
def login():
    loginform = LogInForm()
    if loginform.validate_on_submit():
        user = UserModel.query.filter_by(email=loginform.email.data).first()
        if user and user.check_password(loginform.password.data):
            login_user(user)
            flash(_('Successful login!'), 'success')
            return redirect(url_for('core_bp.inactive'))
        else:
            flash(_('Email or password is incorrect. Please try again.'), 'danger')
    return render_template('base.html', form=loginform)

@core_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('core_bp.base'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_token(user.email)
            reset_token_url = url_for('core_bp.reset_token', token=token, _external=True)
            html = render_template('reset_password_mail/reset_password_mail.html', reset_token_url=reset_token_url)
            subject = _('Exclusive shop password reset request')
            send_email(user.email, subject, html)
            flash(_('An email has been sent with instructions to reset your password.'), 'success')
        else:
            flash(_('That email account is not associated with any account.'), 'danger')
    return render_template('base.html', form=form)

@core_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('core_bp.base'))
    email = confirm_token(token)
    if not email:
        flash(_('This is an invalid or expired token.'), 'danger')
        return redirect(url_for('core_bp.base'))
    user = UserModel.query.filter_by(email=email).first()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        user.save()
        flash(_('Your password has been updated!'), 'success')
        return redirect(url_for('core_bp.login'))
    return render_template('base.html', form=form)

@core_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash(_('Logged out successfully'), 'success')
    return redirect(url_for('core_bp.base'))

@core_bp.route('/verify/<token>')
@login_required
def verify_email(token):
    if current_user.is_verified:
        flash(_('Account is already verified.'), 'success')
        return redirect(url_for('core_bp.base'))
    email = confirm_token(token)
    user = UserModel.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_verified = True
        user.save()
        login_user(user)
        flash(_('You have verified your account. Thanks!'), 'success')
    else:
        flash(_('The confirmation link is invalid or has expired.'), 'danger')
    return redirect(url_for('core_bp.base'))

@core_bp.route('/resend_email_verification/')
@login_required
def resend_email_verification():
    if current_user.is_verified:
        flash(_('Your account is already verified'), 'success')
        return redirect(url_for('core_bp.base'))
    token = generate_token(current_user.email)
    verify_url = url_for('core_bp.verify_email', token=token, _external=True)
    html = render_template('verify_email/verify_email.html', verify_url=verify_url)
    subject = _('Please confirm your email')
    send_email(current_user.email, subject, html)
    flash(_('A new confirmation email has been sent.'), 'success')
    return redirect(url_for('core_bp.base', token=token))

@core_bp.route('/inactive')
@login_required
def inactive():
    if current_user.is_verified:
        return redirect(url_for('core_bp.base'))
    return render_template('base.html')

@core_bp.route('/about')
def about():
    return render_template('base.html')

@core_bp.route('/account/profile', methods=["GET", "POST"])
@login_required
def profile():
    if not current_user.is_verified:
        flash(_('To access the account page you must be verified'), 'danger')
        return redirect(url_for('core_bp.inactive'))
    
    form = EditUserForm()
    form.firstName.render_kw = {'placeholder': current_user.firstName}
    form.lastName.render_kw = {'placeholder': current_user.lastName if current_user.lastName else '(Undefined)'}
    form.email.render_kw = {'placeholder': current_user.email}
    form.address.render_kw = {'placeholder': current_user.address if current_user.address else '(Undefined)'}

    if form.validate_on_submit():
        existing_account = UserModel.query.filter_by(email=form.email.data).first()

        if not existing_account or existing_account.id == current_user.id:
            current_user.firstName = form.firstName.data if form.firstName.data else current_user.firstName
            current_user.lastName = form.lastName.data if form.lastName.data else current_user.lastName
            current_user.email = form.email.data if form.email.data else current_user.email
            current_user.address = form.address.data if form.address.data else current_user.address

            if form.password.data and current_user.check_password(form.password.data):
                if form.newPassword.data:
                    current_user.password = generate_password_hash(form.newPassword.data)

            current_user.save()
            flash(_('Saved changes successfully'), 'success')
            return redirect(url_for('core_bp.profile'))
        else:
            flash(_('Account already exists with this email'), 'danger')
    return render_template('base.html', form=form)
