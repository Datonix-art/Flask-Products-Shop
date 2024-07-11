import os
from flask import Blueprint, jsonify, redirect, render_template, flash, current_app, request, url_for
from flask_login import login_required, current_user
from store.shop.models import OrderModel, ProductModel, db, CategoryModel, FavoriteProductModel
from store.shop.forms import BuyingForm, CheckoutForm
from store.cart.models import CartModel
from datetime import datetime, timedelta
import json

shop = Blueprint('shop', __name__, template_folder='templates')

def set_expiration_time():
    current_app.config['expiration_time'] = datetime.now() + timedelta(days=3, hours=23, minutes=59, seconds=59)

set_expiration_time()

def get_remaining_time_in_seconds():
    remaining_time = current_app.config['expiration_time'] - datetime.now()
    remaining_time_in_seconds = remaining_time.total_seconds()
    if remaining_time_in_seconds <= 0:
        set_expiration_time()
        remaining_time_in_seconds = (current_app.config['expiration_time'] - datetime.now()).total_seconds()
    return remaining_time_in_seconds

@shop.route('/remaining_time')
def remaining_time():
    remaining_time_in_seconds = get_remaining_time_in_seconds()
    return jsonify({'remaining_time_in_seconds': remaining_time_in_seconds})

@shop.route('/all_products/<int:page_id>', methods=["GET", "POST"])
def all_products(page_id):
    try:
        json_data_file_path = os.path.join(current_app.root_path, 'static', 'data/products.json')

        with open(json_data_file_path, 'r') as file:
            json_data = json.load(file)

        categorys = json_data.get('category')

        for category_data in categorys:
            category = CategoryModel.query.get(category_data['id'])
            if not category:
                category = CategoryModel(
                   id = category_data['id'],
                   name = category_data['name']
                )
                category.create()
            else: continue

        products = json_data.get('products')

        for product_data in products:
            existing_product = ProductModel.query.get(product_data['id'])
            if not existing_product:
                products = ProductModel(
                   id = product_data['id'],
                   category_id = product_data['category_id'],
                   name = product_data['name'],
                   slug = product_data['slug'],
                   description = product_data['description'],
                   image = product_data['image'],
                   price = product_data['price'],
                   amount = product_data['amount']
                )

                products.create()
            else: continue

    except Exception as e:
        db.session.rollback()
        flash(f'Failed to add products to the model. error message: {e}', 'danger')

    all_products = ProductModel.query.paginate(per_page=12, page=page_id)
    return render_template('base.html', products = all_products)

@shop.route('/add_to_favorite/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_to_favorite(product_id):
    product = FavoriteProductModel.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if product:
        flash('Product is already added to the favorites', 'danger')
    else:
        favorite_product = FavoriteProductModel(product_id=product_id, user_id=current_user.id)
        favorite_product.create()
        flash('Succesfully added product to favorites', 'success')
    return redirect(url_for('shop.favorite_products'))   
    
@shop.route('/favorite_products')
@login_required
def favorite_products():
    favorite_products = FavoriteProductModel.query.filter_by(user_id=current_user.id).all()
    return render_template('base.html', favorite_products=favorite_products)

@shop.route('/delete_from_favorites/<int:product_id>')
@login_required
def delete_from_favorites(product_id):
    product = FavoriteProductModel.query.filter_by(product_id=product_id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Succesfully deleted product from favorites', 'success')
    return redirect(url_for('shop.favorite_products'))

@shop.route('/clear_favorites', methods=['GET', 'POST'])
@login_required
def clear_favorites():
    products = FavoriteProductModel.query.filter_by(user_id=current_user.id).all()
    for product in products:
        product.delete()
    flash('Favorites cleared succesfully', 'success')
    return redirect(url_for('shop.favorite_products'))

@shop.route('/product_details/<int:id>', methods=['GET', "POST"])
def inner_product(id):
    form = BuyingForm()
    product = ProductModel.query.get_or_404(id)
    if form.validate_on_submit():
        pass
    return render_template('base.html', product=product, form=form)

@shop.route('/category_product/<int:category_id>/<int:page_id>', methods=["GET"])
def category_product(category_id, page_id):
    category = ProductModel.query.get_or_404(category_id)
    category_product = ProductModel.query.filter_by(category_id=category.id).paginate(per_page=8, page=page_id)
    return render_template('base.html', category=category, category_product=category_product)

@shop.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    user_id = current_user.id
    cart_items = CartModel.query.filter_by(user_id=user_id).all()
    products = []
    total_price = 0

    for item in cart_items:
        product = ProductModel.query.get(item.product_id)
        product.amount = item.amount
        total_price += product.amount * product.price
        products.append(product)

    if form.validate_on_submit():
        total_price = sum(product.price * item.amount for item in cart_items)

        order = OrderModel(
              user_id=user_id,
              first_name=form.first_name.data,
              company_name=form.company_name.data,
              street_address=form.street_address.data,
              apartment=form.apartment.data,
              town_city=form.town_city.data,
              number=form.number.data,
              email=form.email.data,
              total_price=total_price
        )

        order.create()

        flash('Order created succesfully!', 'success')
        return redirect(url_for('core.base', order_id=order.id))
    return render_template('base.html', form=form, total_price=total_price, cart=products)
