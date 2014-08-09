from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import validators, ValidationError, TextField, TextAreaField, SubmitField, PasswordField, SelectMultipleField, FormField, SelectField

class RegistrationForm(Form):
  email = EmailField('Email', [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email address.")])
  pass1 = PasswordField('Password', [validators.Required("Please enter a password.")])
  pass2 = PasswordField('Repeat Password', [validators.Required("Please repeat your password.")])

  def validate(self):
    if not Form.validate(self):
      return False
    if self.pass1.data != self.pass2.data:
      self.pass1.errors.append("Please retype your password - they didn't match")
      return False 
    return True
  
class LoginForm(Form):
  email = EmailField('Email', [validators.Required("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter your password.")])

  def validate(self):
    if not Form.validate(self):
      return False
    return True
