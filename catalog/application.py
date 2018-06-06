from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
import random, string, httplib2, json, requests, os
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError

# CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello World!'

@app.route('/catalog')
def catalogHome():
    return 'This will show overall categories and latest items'

@app.route('/catalog/<str:category>')
@app.route('/catalog/<str:category>/items')
def categoryItems():
    return 'This will show a category spec. items'

@app.route('/catalog/<str:category>/<str:item_name>')
def itemInfo():
    return 'This will show item info'

@app.route('/catalog/<str:item_name>/edit')
def editItem(item_name):
    return 'This page when logged in allows item editing'

@app.route('/catalog/<str:item_name>/delete')
def deleteItem(item_info):
    return 'Delete item page when logged in'

@app.route('/catalog.json')
def jsonCatalog():
    return 'Jsonify/serialized item catalog info'

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(port=8000, debug=True)
