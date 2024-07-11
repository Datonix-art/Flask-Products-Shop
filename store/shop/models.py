from store.core.models import UserModel
from store.base_model import BaseModel
from store import db
from sqlalchemy import func

class CategoryModel(db.Model, BaseModel):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    products = db.relationship('ProductModel', back_populates='category', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

class ProductModel(db.Model, BaseModel):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('CategoryModel', back_populates='products')
    name = db.Column(db.String(30), nullable=False, unique=True)
    slug = db.Column(db.String(300), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(128), nullable=True, unique=True)
    price = db.Column(db.Integer, nullable=False, default=1000)
    amount = db.Column(db.Integer, nullable=False, default=1)
    carts = db.relationship('CartModel', back_populates='product')
    favorites = db.relationship('FavoriteProductModel', back_populates = 'product')

    def __repr__(self):
        return f'id: {self.id} - Name: {self.name} - Rs. {self.price}'

class OrderModel(db.Model, BaseModel):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(15), nullable=False)
    company_name = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(30), nullable=False)
    apartment = db.Column(db.String(30))
    town_city = db.Column(db.String(30), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'id:{self.id} ,user id:{self.user_id}, number:{self.number}, email: {self.email}, total price: {self.total_price}, create: {self.created_at}'

class FavoriteProductModel(db.Model, BaseModel):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product = db.relationship('ProductModel', back_populates='favorites')
