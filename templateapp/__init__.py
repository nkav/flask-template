# all the imports
import sqlite3
import os.path as op
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin

app = Flask(__name__)

"""Configure application instance from app.cfg and overwrite with
   any instance specific settings.
     
   Set up environment variable on Linux and OSX by using:

     $ export YOURAPPLICATION_SETTINGS='/path/to/config/file'
"""
app.config.from_pyfile('app.cfg')
app.config.from_envvar('TEMPLATEAPP_SETTINGS', silent=True)

db = SQLAlchemy(app)

import models

# Create Database if doesn't already exist
if not op.isfile(app.config['SQLALCHEMY_DATABASE_NAME'][0]):
  with app.app_context():
    db.create_all()

# Enable Django Admin-like interface for the Users Model...
admin = Admin(app)
admin.add_view(ModelView(models.User, db.session))

# ... and also static files.
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

import routes
