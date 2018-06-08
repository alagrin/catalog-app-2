from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
from flask_security import login_required
import random, string, httplib2, json, requests, os
# import auth, db_setup to create database upon running app

# CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)

# Views
@app.route('/')
def main():
    return 'Hello World!'

@app.route('/register')
def userRegister():
    return 'Page for login/user registration, shows form'

@app.route('/login')
def login():
    return 'Template for user login/registration'

@app.route('/logout')
def logout():
    return 'User taken here upon clicking log out'

@app.route('/catalog')
def catalogHome():
    return render_template('categories.html')

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
    app.secret_key = os.urandom(12)
    app.run(port=8000, debug=True)
