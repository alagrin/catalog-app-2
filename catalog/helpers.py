from functools import wraps
from flask import session as login_session, request, redirect, url_for
import random

def gen_random_string(valid, length):
        random_string = ''.join(valid) # join together members of tuple which is iterable
        return ''.join(random.choice(random_string) for x in range(length)) # returns a random string w/ length chars

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in login_session:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

# def getUserID(email):
#     try:
#         user = session.query(User).filter_by(email=email).one()
#         return user.id
#     except:
#         return None

# def createUser(login_session):
#     newUser = User(
#         name=login_session['username'],
#         email=login_session['email'],
#         picture=login_session['picture'])
#     session.add(newUser)
#     session.commit()
#     user = session.query(User).filter_by(email=login_session['email']).one()
#     return user.id