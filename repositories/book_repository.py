from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING
import datetime

from models.book import Book
from models.author import Author
from models.order_book import OrderBook
from models.publisher import Publisher
from models.category import Category
from models.bookstore_shelf import BookstoreShelf
from models.bookstore import Bookstore

def create_book(session: Session, isbn: int, title: str, price: float, publication_date:datetime.datetime, category_id: int, author_id: int, publisher_id: int):
    book = Book(isbn=isbn, title=title, price=price, publication_date=publication_date, category_id=category_id, author_id=author_id, publisher_id=publisher_id)
    session.add(book)
    return book

def get_book_by_isbn(session:Session, isbn:int):
    stmt = select(Book).where(Book.isbn == isbn)
    book = session.execute(stmt).scalar_one_or_none()
    return book

def get_book_by_id(session:Session, id:int):
    stmt = select(Book).where(Book.id == id)
    book = session.execute(stmt).scalar_one_or_none()
    return book

def get_all_books(session:Session):
    stmt = select(Book).options(joinedload(Book.author), joinedload(Book.publisher), joinedload(Book.category))
    books = session.execute(stmt).scalars().all()
    return books

def get_all_books_of_author(session:Session, author_name:str):
    stmt = select(Book).join(Book.author).where(Author.name == author_name).options(joinedload(Book.publisher), joinedload(Book.category))
    books = session.execute(stmt).scalars().all()
    return books

def get_all_books_of_publisher(session:Session, publisher_name:str):
    stmt = select(Book).join(Book.publisher).where(Publisher.name == publisher_name).options(joinedload(Book.author), joinedload(Book.category))
    books = session.execute(stmt).scalars().all()
    return books

def get_all_books_of_category(session:Session, category_name:str):
    stmt = select(Book).join(Book.category).where(Category.name == category_name).options(joinedload(Book.author), joinedload(Book.publisher))
    books = session.execute(stmt).scalars().all()
    return books

def get_all_books_of_bookstore(session:Session, bookstore_name:str, country_identifier:str):
    stmt = (select(Book, BookstoreShelf.quantity).distinct()
            .join(Book.bookstore_shelves).join(BookstoreShelf.bookstore)
            .where(Bookstore.name == bookstore_name)
            .options(joinedload(Book.category), joinedload(Book.author), joinedload(Book.publisher))
    )
    books = session.execute(stmt).unique().all()
    return books

def get_book_by_sales(session:Session):
    stmt = (
        select(Book, func.coalesce(func.sum(OrderBook.quantity), 0).label("total_sales"))
        .outerjoin(OrderBook.book)
        .group_by(Book.id)
        .order_by(func.sum(OrderBook.quantity).desc())
    )
    books = session.execute(stmt).all()
    return books