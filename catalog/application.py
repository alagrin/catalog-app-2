from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
from flask_security import login_required
import random, string, httplib2, json, requests, os
from db_setup import Base, User, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    return 'Links for register or login'

@app.route('/register', methods=['GET', 'POST'])
def userRegister():
    return 'Page for login/user registration, shows form'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        newUser = User(email=request.form['email'], \
        password=request.form['password'])
        session.add(newUser)
        session.commit()

        # set login_session['email'] to email as well, provide to session/ g object

        flash('User created successfully')
        return redirect(url_for('catalogHome')) # will contain user_email context
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    return 'User taken here upon clicking log out'

@app.route('/catalog/')
def catalogHome():
    allItems = session.query(Item).limit(20).all()
    return render_template('categories.html', allItems=allItems)

@app.route('/catalog/<category>/')
@app.route('/catalog/<category>/items')
def categoryItems(category):
    # this method has no edit/delete options unless logged in
    itemsByCategory = session.query(Item).filter_by(category=category).all()
    return render_template('categories.html', category=category, \
    items=itemsByCategory)

@app.route('/catalog/<category>/item/new', methods=['GET', 'POST'])
def newItem(category):
    if request.method == 'POST':
        itemToAdd = Item(name=request.form['name'], \
        category=request.form['categories'], description=\
        request.form['description'])
        session.add(itemToAdd)
        session.commit()
        flash('Item added')
        return redirect(url_for('categoryItems', category=category))
    else:
        return render_template('newitem.html', category=category)

# confirm this one below is right, need unique item w/ id to find
@app.route('/catalog/<category>/<int:item_id>/edit', methods=['GET', 'POST'])
# @login_required
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
# @login_required
def deleteItem(category, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item deleted')
        return redirect(url_for('categoryItems', category=category))
    else:
        return render_template('delete_item.html', item=itemToDelete)

@app.route('/catalog.json/')
def jsonCatalog():
    return 'Jsonify/serialized item catalog info'

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(port=8000, debug=True)
