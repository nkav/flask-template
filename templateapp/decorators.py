from functools import wraps
from flask import session, request, url_for, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            # Forward to login page; next is the original page accessed
            if '/logout' not in request.url:
              flash('Please first login.')
              return redirect(url_for('login', next=request.url))
            # Only exception is if the user tries to logout
            else:
              return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def anon_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
