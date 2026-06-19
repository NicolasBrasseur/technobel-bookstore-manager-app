from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.bookstore_shelf import BookstoreShelf

def create_bookstore_shelf(session: Session, quantity: int, bookstore_id: int, book_id: int):
    bookstore_shelf = BookstoreShelf(session=session, quantity=quantity, bookstore_id=bookstore_id, book_id=book_id)

    try:
        session.add(bookstore_shelf)
        session.commit()
        session.refresh(bookstore_shelf)

    except IntegrityError as exc:
        print("Unexpected error : cannot create bookstore_shelf")
        session.rollback()
        return None

    return bookstore_shelf