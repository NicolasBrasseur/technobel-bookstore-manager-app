from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.bookstore_shelf import BookstoreShelf

def create_bookstore_shelf(session: Session, quantity: int, bookstore_id: int, book_id: int):
    bookstore_shelf = BookstoreShelf(quantity=quantity, bookstore_id=bookstore_id, book_id=book_id)
    session.add(bookstore_shelf)
    session.flush()
    return bookstore_shelf

def get_bookstore_shelf(session:Session, bookstore_id:int, book_id:int):
    stmt = select(BookstoreShelf).where(BookstoreShelf.bookstore_id == bookstore_id, BookstoreShelf.book_id == book_id)
    shelf = session.execute(stmt).scalar_one_or_none()
    return shelf