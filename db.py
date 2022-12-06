import pymysql
from sqlalchemy.dialects.mysql import VARCHAR

from sqlalchemy import create_engine, ForeignKey, Text, Enum
from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from enum import Enum as enum

from marshmallow import *

engine = create_engine("mysql+pymysql://root:147258369@localhost:3306/labs4_10", echo=True)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
base = declarative_base()

# Without foreign keys
class BookStatus(enum):
    available = "available"
    pending = "pending"


class Genre(base):
    __tablename__ = "genre"

    genre_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(60), nullable=False)

    def __init__(self, name):
        self.name = name


class Author(base):
    __tablename__ = "author"

    author_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(60), nullable=False)
    last_name = Column(VARCHAR(60), nullable=False)
    birth_date = Column(Date)
    country = Column(VARCHAR(80), nullable=False)

    def __init__(self, first_name, last_name, birth_date, country):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.country = country

# with fk

class Book(base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(80), nullable=False)
    year = Column(Date, nullable=False)
    language = Column(VARCHAR(60), nullable=False)

    status = Column(Enum(BookStatus), nullable=False)
    description = Column(VARCHAR(80), nullable=True)
    photo_url = Column(VARCHAR(100), nullable=True)
    price = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey("author.author_id"), nullable=False)
    id_genre = Column(Integer, ForeignKey('genre.genre_id'), nullable=False)

    def __init__(self, name, year, language, id_genre, author_id,
                 status, description, photo_url, price):
        self.name = name
        self.year = year
        self.language = language
        self.id_genre = id_genre
        self.author_id = author_id
        self.status = status
        self.price = price
        self.description = description
        self.photo_url = photo_url

    @classmethod
    def post_book(cls, item):
        with Session() as session:
            # find_book_response = Books.get_book_by_id(item.book_id)
            # if find_book_response != 404:
                session.add(item)
                session.commit()
                return 200
            # else:
            #     return 404

    @classmethod
    def update_book(cls, book_id, updates):
        with Session() as session:
            if cls.get_book_by_id(book_id) == 404:
                return 404

            session.query(Book).filter(Book.book_id == book_id).update(updates)
            session.commit()
            return 200

    @classmethod
    def get_books(cls):
        with Session() as session:
            return session.query(cls).all()
    
    @classmethod
    def get_book_by_id(cls, id):
        with Session() as session:
            class_id_attr = f"{cls.__name__}_id".lower()
            class_object = session.query(cls).filter(getattr(cls, class_id_attr) == id).first()
            if class_object == None:
                return 404
            return class_object
    
    @classmethod
    def get_book_by_status(cls, status):
        with Session() as session:
            class_id_attr = "status"
            class_object = session.query(cls).filter(getattr(cls, class_id_attr) == status).first()
            if class_object == None:
                return 404
            return class_object

    @classmethod
    def get_book_by_genre(cls, genre):
        with Session() as session:
            class_id_attr = "id_genre"
            class_object = session.query(cls).filter(getattr(cls, class_id_attr) == genre).first()
            if class_object == None:
                return 404
            return class_object

    @classmethod
    def get_book_by_author(cls, author_id):
        with Session() as session:
            class_id_attr = "author_id"
            class_object = session.query(cls).filter(getattr(cls, class_id_attr) == author_id).first()
            if class_object == None:
                return 404
            return class_object

    @classmethod
    def get_book_by_name(cls, name):
        with Session() as session:
            class_id_attr = "name"
            class_object = session.query(cls).filter(getattr(cls, class_id_attr) == name).first()
            if class_object == None:
                return 404
            return class_object

    @classmethod
    def delete_book(cls, id):
        with Session() as session:
            class_object = cls.get_book_by_id(id)
            if class_object == 404:
                return 404
            class_id_attr = f"{cls.__name__}_id".lower()
            session.query(cls).filter(getattr(cls, class_id_attr) == id).delete()
            session.commit()
            return 200


class BookSchema(Schema):
    book_id = fields.Integer()
    name = fields.String()
    year = fields.Date()
    language = fields.String()

    status = fields.Enum(BookStatus)
    description = fields.String()
    photo_url = fields.String()
    price = fields.Integer()

    id_genre = fields.Integer()
    author_id = fields.Integer()


class BookHasAuthors(base):
    __tablename__ = "book_has_authors"

    id_book = Column(Integer, ForeignKey('book.book_id'), nullable=False, primary_key=True)
    id_author = Column(Integer, ForeignKey('author.author_id'), nullable=False, primary_key=True)

    def __init__(self, id_book, id_author):
        self.id_book = id_book
        self.id_author = id_author


class Order(base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True)
    full_name = Column(VARCHAR(120), nullable=False)
    email = Column(VARCHAR(120), nullable=False)
    phone = Column(VARCHAR(25), nullable=False)
    id_book = Column(Integer, ForeignKey('book.book_id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, full_name, email, phone, id_book, quantity):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.id_book = id_book
        self.quantity = quantity

class Admin(base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(60), unique=True, nullable=False)
    token = Column(VARCHAR(256), nullable=False)

    def __init__(self,  username, token):
        self.username = username
        self.token = token

    @classmethod
    def auth(cls, username, token):
        with Session() as session:
            admin = session.query(cls).filter((cls.username == username and
                                                    cls.token == token)).first()
            if admin:
                return admin
            else:
                return False

class AdminSchema(Schema):
    admin_id = fields.Integer()
    user_name = fields.String()
    full_name = fields.String()
    token = fields.String()

if __name__ == "__main__":
    # base.metadata.tables["admin"].create(bind = engine)
    pass