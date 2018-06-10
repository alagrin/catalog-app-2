from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
from flask_security import login_required
import random, string, httplib2, json, requests, os
# import auth
from models import User, Item
from db_setup import init_db, db_session

# CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)

# session = db_session(session_factory)
# s = session()

# Views
@app.route('/')
def main():
    return 'Hello World! This is the landing page for item catalog'

@app.route('/register', methods=['GET', 'POST'])
def userRegister():
    return 'Page for login/user registration, shows form'

@app.route('/login', methods=['POST'])
def login():
    return 'Template for user login/registration'

@app.route('/logout')
def logout():
    return 'User taken here upon clicking log out'

@app.route('/catalog')
def catalogHome():
    print(s.query(User).all())
    return 'Catalog home'

@app.route('/catalog/<category>')
@app.route('/catalog/<category>/items')
def categoryItems(category):
    return 'This will show a category spec. items'

@app.route('/catalog/<category>/<item_name>')
def itemInfo(category, item_name):
    return 'This will show item info'

@app.route('/catalog/<item_name>/edit')
# @login_required
def editItem(item_name):
    return 'This page when logged in allows item editing'

@app.route('/catalog/<item_name>/delete')
# @login_required
def deleteItem(item_name):
    return 'Delete item page when logged in'

@app.route('/catalog.json')
def jsonCatalog():
    return 'Jsonify/serialized item catalog info'

if __name__ == '__main__':
    init_db()
    app.secret_key = os.urandom(12)
    app.run(port=8000, debug=True)
