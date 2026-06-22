from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from models.book import Book

if TYPE_CHECKING:
    import datetime

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
    pass

def display_all_books_of_author(session:Session, author_name:str):
    pass

def display_all_books_of_publisher(session:Session, publisher_name:str):
    pass

def display_all_books_of_category(session:Session, category_name:str):
    pass

def display_all_books_of_bookstore(session:Session, bookstore_name:str, country_identifier:str):
    pass

def display_book_price_by_country(session:Session, book_isbn:int, country_identifier:str):
    pass

def display_book_by_sales(session:Session, book_isbn:int):
    pass

# def display_book_publisher(session: Session, book_id:int):
#     stmt = select(Book).options(joinedload(Book.publisher)).where(Book.id == book_id)
#     book = session.execute(stmt).scalar_one_or_none()

#     if book is None:
#         print("No book with this id")
#         return False

#     print(book)
#     print(book.publisher)
#     return True