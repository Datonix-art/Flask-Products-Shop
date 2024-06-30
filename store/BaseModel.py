from store import db

class BaseModel:
  def save(self):
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def create(self):
    db.session.add(self)
    db.session.commit()