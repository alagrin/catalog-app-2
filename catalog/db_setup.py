from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    email = Column(String(120), primary_key=True, unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True) # auto-increment
    name = Column(String(120), nullable=False)
    category = Column(String(120), nullable=False)
    added_at = Column(DateTime(), default=datetime.datetime.utcnow, nullable=False)
    user_email = Column(Integer, ForeignKey('users.email'))
    user = relationship(
        "User", backref=backref("users", cascade="all, delete"))

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)

# will need to serialize item info for the json endpoint