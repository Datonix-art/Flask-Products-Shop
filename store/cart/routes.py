from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from store.cart.models import CartModel, db
from store.cart.forms import CartForm, CartItemForm
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
    cart_item.delete()

  return redirect(url_for('cart.shopping_cart'))


@cart.route('/cart/update_cart', methods=['GET', 'POST'])
@login_required
def update_cart():
  user_id = current_user.id
  cart_items = CartModel.query.filter_by(user_id=user_id).all()
  form = CartForm()

  if form.validate_on_submit():
    total_price = 0
    for item_form in form.items:
      item_id = item_form.item_id.data
      new_amount = item_form.new_amount.data
       
      print(f"item_id: {item_id}, new_amount: {new_amount}")

      cart_item = None
      
      for item in cart_items:
        if item.id == item_id:
          cart_item = item
        else:
          flash('error', 'danger')


      if cart_item:
        cart_item.amount = new_amount
        cart_item.save()

        product = ProductModel.query.get(cart_item.product_id)
        total_price += cart_item.amount * product.price 
      else:
        flash(f'cart item {item_id} not found!', 'danger')
    flash('Cart updated successfully!', 'success')
  else:
    flash('Error updating cart!', 'danger')
    for errors in form.errors.items():
      for error in errors:
        flash(f'Error in field {error}', 'danger')
  
  return redirect(url_for('cart.shopping_cart'))
