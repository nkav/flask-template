from flask import request
from app import app

with app.test_request_context('/hello', method='POST'):
  assert request.path == '/hello'
  assert request.method == 'POST'
