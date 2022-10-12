import pymysql
from sqlalchemy.dialects.mysql import VARCHAR

from sqlalchemy import create_engine, ForeignKey, Text, Enum
from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum as enum

engine = create_engine("mysql+pymysql://root:rootadmin2022@localhost:3306/bookShop", echo=True)

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
    description = Column(Text)
    photo_url = Column(Text)
    price = Column(Integer, nullable=False)

    id_genre = Column(Integer, ForeignKey('genre.genre_id'), nullable=False)

    def __init__(self,  year, language, id_genre,
                 status, description, photo_url, price):
        self.year = year
        self.language = language
        self.id_genre = id_genre
        self.status = status
        self.price = price
        self.description = description
        self.photo_url = photo_url


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


if __name__ == "__main__":
    # base.metadata.tables["admin"].create(bind = engine)
    pass