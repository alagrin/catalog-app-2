from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
# from flask_security import login_required
from helpers import filterByCategory
import random, string, httplib2, json, requests, os
from db_setup import Base, User, Item
from sqlalchemy import create_engine, desc
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
    return render_template('base.html')

@app.route('/login', methods=['GET','POST'])
def login():
    # session.rollback()
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
        return render_template('login.html')

@app.route('/logout')
def logout():
    login_session.pop('logged_in', None)
    return redirect(url_for('main'))

@app.route('/catalog/', methods = ['GET', 'POST'])
def catalogHome():
    categories = ['home', 'sports', 'clothing', 'business', 'personal']
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
    # TODO: Suddenly item info won't work, item found but template doesn't load
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
        return render_template('delete_item.html', item=itemToDelete, item_id=item_id, category=category)

@app.route('/catalog.json/')
def jsonCatalog():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(port=8000, debug=True)
