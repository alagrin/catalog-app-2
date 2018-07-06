from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
from helpers import gen_random_string
import random, string, httplib2, json, requests, os
from db_setup import Base, User, Item
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())\
['web']['client_id']
APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db', \
connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Views
@app.route('/')
def main():
    return render_template('base.html')

@app.route('/login', methods=['GET','POST'])
def login():
    # session.rollback()
    valid = (string.ascii_letters, string.digits, ':*&^') # for google login
    state = gen_random_string(valid, 32) # set state to the result of the func above
    login_session['state'] = state # passing value of state to the login_session- preventing CSF attacks

    if request.method == 'POST':
        newUser = User(email=request.form['email'], \
        password=request.form['password'])
        session.add(newUser)
        session.commit()

        login_session['email'] = newUser.email
        login_session['password'] = newUser.password
        login_session['logged_in'] = True
        flash('User created successfully')
        print("user added")
        return redirect(url_for('catalogHome')) # will contain user_email context
    else:
        return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():
    login_session.pop('logged_in', None)
    return redirect(url_for('main'))

@app.route('/catalog/', methods = ['GET', 'POST'])
def catalogHome():
    categories = ['home', 'sports', 'clothing', 'business', 'personal'] #adjust this/ clean up
    allItems = session.query(Item).order_by(desc(Item.added_at)).limit(20).all()
    totalItems = session.query(Item).count()
    # TODO: add categories rep to loop through and show active categories
    # categories = session.query(Item).filter_by(category=category)
    return render_template('categories.html', items=allItems, categories=categories, count=totalItems)

@app.route('/catalog/<category>/')
@app.route('/catalog/<category>/items/')
def categoryItems(category):
    # this different endpoint necessary? trying to separate logged in views and general view
    itemsByCategory = session.query(Item).filter_by(category=category).all()
    itemCount = session.query(Item).filter_by(category=category).count()
    return render_template('categories.html', category=category, \
    items=itemsByCategory, count=itemCount)

@app.route('/catalog/<category>/<int:item_id>')
def itemInfo(category, item_id):
    try:
        item = session.query(Item).filter_by(id=item_id).one()
        if item:
            return render_template('show_item.html', category=category, item=item)
    except Exception as e:
	    return(str(e)) #TODO better way to do this?

@app.route('/catalog/item/new', methods=['GET', 'POST']) #took out <category> in link/function, categ=categ in if
def newItem():
    if request.method == 'POST':
        itemToAdd = Item(name=request.form['name'], \
        category=request.form['categories'], description=\
        request.form['description'])
        session.add(itemToAdd)
        session.commit()
        flash('Item added')
        # return redirect(url_for('categoryItems', item=itemToAdd, category=itemToAdd.category))
        return redirect(url_for('catalogHome'))
    else:
        return render_template('newitem.html')

@app.route('/catalog/<category>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category, item_id):
    itemToEdit = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['categories']:
            itemToEdit.category = request.form['categories']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        session.add(itemToEdit)
        session.commit()
        flash('Updated item info')
        return redirect(url_for('categoryItems', category=category))
    else:
        return render_template('edit_item.html', item=itemToEdit, \
        item_id=item_id, category=category)

@app.route('/catalog/<category>/<item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item deleted')
        return redirect(url_for('categoryItems', category=category))
    else:
        return render_template('delete_item.html', item=itemToDelete, item_id=item_id, category=category)

@app.route('/catalog.json/')
def jsonCatalog():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    authCode = request.data
    print("access token received as {}".format(authCode))

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(authCode)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['logged_in'] = True

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(port=8000, debug=True)
