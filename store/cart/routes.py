from flask import Blueprint, render_template, jsonify, redirect, url_for, session, request, flash
from flask_login import current_user, login_required
from store.cart.models import CartModel, db
from store.cart.forms import CartForm
from store.shop.models import ProductModel

cart = Blueprint('cart', __name__, template_folder='templates')

@cart.app_template_filter('truncate')
def truncate(s, length=15):
  if len(s) > length:
    return s[:length] + '...'
  return s

@cart.route('/cart')
@login_required
def shopping_cart():
  user_id = current_user.id
  cart_items = CartModel.query.filter_by(user_id=user_id).all()
  products = []
  total_price = 0
  form = CartForm()
  for item in cart_items:
    product = ProductModel.query.get(item.product_id)
    product.amount = item.amount
    total_price += product.amount * product.price
    products.append(product)
  return render_template('base.html', cart=products,  total_price=total_price, form=form)

@cart.route('/<int:product_id>/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
  user_id = current_user.id
  cart_item = CartModel.query.filter_by(user_id = user_id, product_id = product_id).first()

  if cart_item:
    cart_item.amount += 1
    cart_item.create()
    flash('succesfully increased amount of product in cart', 'success')
  else:
    cart = CartModel(product_id=product_id, user_id=user_id, amount=1)
    cart.create()
    flash('succesfully added product to the cart', 'success')
      
  return redirect(url_for('cart.shopping_cart'))

@cart.route('/cart/<int:product_id>/remove_from_cart', methods=["GET", "POST"])
@login_required
def remove_from_cart(product_id):
  user_id = current_user.id
  cart_items = CartModel.query.filter_by(user_id=user_id, product_id=product_id).all()

  for cart_item in cart_items:
    cart_item.delete()

  return redirect(url_for('cart.shopping_cart'))

@cart.route('/cart/clear_cart', methods=['GET', 'POST'])
@login_required
def cleart_cart():
  user_id = current_user.id
  cart_items = CartModel.query.filter_by(user_id=user_id).all()

  for cart_item in cart_items:
    cart_item.remove()

  return redirect(url_for('cart.shopping_cart'))


@cart.route('/cart/update_cart', methods=['POST'])
@login_required
def update_cart():
  user_id = current_user.id
  cart_items = CartModel.query.filter_by(user_id=user_id).all()
  form = CartForm()

  if form.validate_on_submit():
    total_price = 0
    for item in cart_items:
      item.amount = form.new_amount.data
      item.save()
      product = ProductModel.query.get(item.product_id)
      total_price += item.amount * product.price
      flash('Cart updated successfully!', 'success')
      return redirect(url_for('cart.shopping_cart'))
  
  flash('Error updating cart!', 'danger')
  return redirect(url_for('cart.shopping_cart'))
