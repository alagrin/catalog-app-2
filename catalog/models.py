from sqlalchemy import Column, Integer, String
from db_setup import Base
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, \
# login_required, RoleMixin

#Definition of models
class User(Base):
    __tablename__ = 'users'
    email = Column(String(120), primary_key=True, unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True) # auto-increment
    name = Column(String(120), nullable=False)
    category = Column(String(120), nullable=False)
    added_at = Column(String(120), nullable=False)

# Serialize for access via JSON endpoint

# Set up Flask Security

# user_datastore = SQLAlchemyUserDatastore(db, User, Item)
# security = Security(app, user_datastore)
