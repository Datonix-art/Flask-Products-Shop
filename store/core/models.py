from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 
from store import db
from store.base_model import BaseModel

class ContactModel(db.Model, BaseModel):
   __tablename__ = 'contacts'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String, unique=False, nullable=False)
   email = db.Column(db.String, unique=False, nullable=False)
   phoneNumber = db.Column(db.Integer, unique=False, nullable=False)
   message = db.Column(db.String, nullable=False, unique=False)

   def __repr__(self):
      return self.name + self.email + self.phoneNumber + self.message

class UserModel(db.Model, BaseModel, UserMixin):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key=True)
   firstName = db.Column(db.String, nullable=False, unique=False)
   lastName = db.Column(db.String, nullable=True)
   email = db.Column(db.String, nullable=False, unique=True)
   address = db.Column(db.String, nullable=True)
   password = db.Column(db.String, nullable=False, unique=False)

   def __init__(self, firstName, lastName, email, address, password):
      self.firstName = firstName
      self.lastName = lastName
      self.email = email
      self.address = address
      self.password = generate_password_hash(password)

   def check_password(self, password):
      return check_password_hash(self.password, password)
   
   def __repr__(self):
      return self.email
