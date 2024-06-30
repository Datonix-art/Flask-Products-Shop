from store.BaseModel import BaseModel, db

class CartModel(db.Model, BaseModel):
  __tablename__ = 'carts'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
  amount = db.Column(db.Integer, default=1)

  def __repr__(self):
    return f'user id: {self.user_id}; product id: {self.product_id}'
  
  def update_amount(self, amount):
    self.amount += amount
    
  