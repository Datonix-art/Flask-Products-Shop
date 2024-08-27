from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from store.cart.models import CartModel, db
from store.shop.models import ProductModel
from flask_babel import _

cart_bp = Blueprint('cart_bp', __name__, template_folder='templates')

@cart_bp.app_template_filter('truncate')
def truncate(s, length=15):
    if len(s) > length:
        return s[:length] + '...'
    return s

@cart_bp.route('/cart')
@login_required
def shopping_cart():
    user_id = current_user.id
    cart_items = CartModel.query.filter_by(user_id=user_id).all()
    products = []
    total_price = 0

    for item in cart_items:
        product = ProductModel.query.get(item.product_id)
        product.amount = item.amount
        total_price += product.amount * product.price
        products.append(product)
    return render_template('base.html', cart=products,  total_price=total_price)

@cart_bp.route('/<int:product_id>/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
    user_id = current_user.id
    cart_item = CartModel.query.filter_by(user_id = user_id, product_id = product_id).first()

    if cart_item:
        cart_item.amount += 1
        cart_item.create()
        flash(_('succesfully increased amount of product in cart'), 'success')
    else:
        cart = CartModel(product_id=product_id, user_id=user_id, amount=1)
        cart.create()
        flash(_('succesfully added product to the cart'), 'success')
      
    return redirect(url_for('cart_bp.shopping_cart'))

@cart_bp.route('/cart/<int:product_id>/remove_from_cart', methods=["GET", "POST"])
@login_required
def remove_from_cart(product_id):
    user_id = current_user.id
    cart_items = CartModel.query.filter_by(user_id=user_id, product_id=product_id).all()

    for cart_item in cart_items:
        cart_item.delete()

    return redirect(url_for('cart_bp.shopping_cart'))

@cart_bp.route('/cart/clear_cart', methods=['GET', 'POST'])
@login_required
def clear_cart():
    user_id = current_user.id
    cart_items = CartModel.query.filter_by(user_id=user_id).all()

    for cart_item in cart_items:
        cart_item.delete()

    return redirect(url_for('cart_bp.shopping_cart'))


@cart_bp.route('/cart/update_cart', methods=['GET','POST'])
@login_required
def update_cart():
    if request.method == "POST":
        user_id = current_user.id
        form = request.form
        total_price = 0
        print(form)

        item_ids = form.getlist('item_id')
        item_amounts = form.getlist('item_amount')
        
        for item_id, item_amount in zip(item_ids, item_amounts):
            print(f'item_id: {item_id}, item_amount: {item_amount}')

            if item_id and item_amount:
                item = CartModel.query.filter_by(user_id=user_id, product_id=item_id).first()
            
                if item:
                    item.amount = item_amount
                    item.save()
                    product = ProductModel.query.get(item.product_id)
                    total_price += item.amount * product.price

        flash(_('Cart updated successfully!'), 'success')
        return redirect(url_for('cart_bp.shopping_cart'))
