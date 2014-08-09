from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from templateapp import db

class NewModel():
  def add_to_db(self):
    db.session.add(self)
    db.session.commit()

class User(NewModel, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True)
  passhash = db.Column(db.String(100))


  def __init__(self, email, password):
    self.email = email
    self.set_password(password)

  def set_password(self, password):
    self.passhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.passhash, password) 

  def __repr__(self):
    return '<User %r>' % self.email

  # Returns User object if username and password are correct, 
  # otherwise returns None

  @classmethod
  def get_user_or_none(cls, email):
    return cls.query.filter(cls.email == email).first()

  @classmethod
  def verify_user_or_none(cls, email, password):
    candidate = cls.get_user_or_none(email)
    if not candidate:
      return None
    elif candidate.check_password(password):
      return candidate 
    else:
      return None

