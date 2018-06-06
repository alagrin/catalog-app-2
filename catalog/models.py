from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, \
login_required, RoleMixin

# Creates app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'my-super-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itemcatalog.db'

# Creates Database connection object
db = SQLAlchemy(app)

#Definition of models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=True, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    added_at = db.Column(db.String(120), nullable=False)

# Set up Flask Security
user_datastore = SQLAlchemyUserDatastore(db, User, Item)
security = Security(app, user_datastore)

# if __name__ == '__main__':
#     app.run()
