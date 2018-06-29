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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    category = Column(String(120), nullable=False)
    description = Column(String(120))
    added_at = Column(DateTime(), default=datetime.datetime.utcnow, nullable=False) #confirm its auto adding this
    user_email = Column(String(120), ForeignKey('users.email'))
    user = relationship("User", backref="users", cascade="all, delete")

    @property # Converting data in database, create JSON object, meet API 
    def serialize(self):
        """Return item data in easily serializable format"""
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description
        }

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
