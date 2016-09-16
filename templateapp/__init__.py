# all the imports
import sqlite3
import os 
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin

app = Flask(__name__)

app.config.from_envvar('TEMPLATEAPP_SETTINGS', silent=True)
app.config.from_object('config')

db = SQLAlchemy(app)

import models

# Create Database if doesn't already exist
if not os.path.isfile(app.config['SQLALCHEMY_DATABASE_PATH']):
  with app.app_context():
    db.create_all()

# Enable Django Admin-like interface for the Users Model...
admin = Admin(app)
admin.add_view(ModelView(models.User, db.session))

# ... and also static files.
path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

import routes
