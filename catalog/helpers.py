from functools import wraps
from flask import session as login_session, request, redirect, url_for
import random

def gen_random_string(valid, length):
        random_string = ''.join(valid)
        return ''.join(random.choice(random_string) for x in range(length))

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in login_session:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function
