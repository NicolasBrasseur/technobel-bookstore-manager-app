from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING
import datetime

from models.book import Book

if TYPE_CHECKING:
    from models.author import Author # Peut etre pas mettre dans type checking
    from models.order_book import OrderBook

def create_book(session: Session, isbn: int, title: str, price: float, publication_date:datetime.datetime, category_id: int, author_id: int, publisher_id: int):
    book = Book(isbn=isbn, title=title, price=price, publication_date=publication_date, category_id=category_id, author_id=author_id, publisher_id=publisher_id)

    try:
        session.add(book)
        session.commit()
        session.refresh(book)

    except IntegrityError as exc:
        print("Unexpected error : cannot create book")
        session.rollback()
        return None

    return book

def get_book_by_isbn(session:Session, isbn:int):
    pass

def display_all_books(session:Session):
    stmt = select(Book).options(joinedload(Book.author, Book.publisher, Book.category))
    books = session.execute(stmt).scalars().all()
    return books

def display_all_books_of_author(session:Session, author_name:str):
    stmt = select(Book).join(Book.author).where(Author.name == author_name)
    books = session.execute(stmt).scalars().all()
    return books


def display_all_books_of_publisher(session:Session, publisher_name:str):
    pass

def display_all_books_of_category(session:Session, category_name:str):
    pass

def display_all_books_of_bookstore(session:Session, bookstore_name:str, country_identifier:str):
    pass


def display_book_by_sales(session:Session, book_isbn:int):
    stmt = (
        select(Book, func.coalesce(func.sum(OrderBook.quantity), 0).label("total_sales"))
        .outerjoin(OrderBook.book)
        .group_by(Book.id)
        .order_by(func.sum(OrderBook.quantity).desc())
    )
    books = session.execute(stmt).scalars().all()
    return books