from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from models.bookstore import Bookstore
from models.book import Book
from models.bookstore_shelf import BookstoreShelf

def create_bookstore(session: Session, name: str, country_identifier: str):
    bookstore = Bookstore(name=name, country_identifier=country_identifier)
    session.add(bookstore)
    return bookstore

def get_bookstore_by_name_and_country(session:Session, name:str, country_identifier:str):
    stmt = select(Bookstore).where(and_(Bookstore.name == name, Bookstore.country_identifier == country_identifier))
    bookstore = session.execute(stmt).scalar_one_or_none()
    return bookstore

def get_bookstore_by_id(session:Session, id:int):
    stmt = select(Bookstore).where(Bookstore.id == id)
    bookstore = session.execute(stmt).scalar_one_or_none()
    return bookstore

def get_all_bookstore_having_book(session:Session, book_isbn:int, country_identifier:str):
    stmt = (select(Bookstore, BookstoreShelf.quantity).distinct()
            .join(Bookstore.shelves)
            .join(BookstoreShelf.book)
            .where(Book.isbn == book_isbn, Bookstore.country_identifier == country_identifier, BookstoreShelf.quantity > 0)
            .options(joinedload(Bookstore.shelves))
    )
    bookstores = session.execute(stmt).unique().all()
    return bookstores