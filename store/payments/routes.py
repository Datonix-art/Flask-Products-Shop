from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from store.cart.models import CartModel
from store.shop.forms import CheckoutForm
from store.shop.models import ProductModel
from flask_babel import _
from dotenv import load_dotenv
import stripe
import os

load_dotenv()

payment_bp = Blueprint('payment_bp', __name__)

def create_stripe_products(product_name, product_description, price_amount):
    product = stripe.Product.create(
        name=product_name,
        description=product_description,
    )

    price = stripe.Price.create(
        product=product.id,
        unit_amount=price_amount,
        currency='usd'
    )

    return product.id, price.id

@payment_bp.route('/checkout', methods=['GET', "POST"])
def checkout():
    if not current_user.is_verified:
        flash(_('To access account page you must be verified'), 'danger')
        return redirect(url_for('core_bp.inactive'))

    form = CheckoutForm()
    user_id = current_user.id
    cart_items = CartModel.query.filter_by(user_id=user_id).all()
    products = []
    total_price = 0
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    stripe_public_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    domain_url = 'http://127.0.0.1:5000/'

    line_items = []

    for item in cart_items:
        product = ProductModel.query.get(item.product_id)
        product.amount = item.amount
        total_price += product.amount * product.price
        products.append(product)

        stripe_product_id, stripe_price_id = create_stripe_products(
            product_name=product.name,
            product_description=product.description,
            price_amount=product.price * 100
        )

        line_items.append({
            'price': stripe_price_id,
            'quantity': item.amount
        })

    if form.validate_on_submit():
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'result?status=success',
                cancel_url=domain_url + 'result?status=cancelled',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items
            )
            return jsonify({'sessionId': checkout_session['id']})
        except Exception as e:
            return jsonify(error=str(e)), 403
    return render_template('base.html', form=form, total_price=total_price, cart=products, stripe_public_key=stripe_public_key)

@payment_bp.route('/result')
def result():
    status = request.args.get('status')
    if status == 'success':
        flash(_('Payment was succesfull'), 'success')
    elif status == 'cancelled':
        flash(_('Payment was cancelled'), 'warning')
    else:
        flash(_('An unknow error occured'), 'danger')

    return redirect(url_for('core_bp.base'))

