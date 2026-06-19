from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.book import Book

def create_book(session: Session, isbn: int, title: str, price: float, category_id: int, author_id: int, publisher_id: int):
    book = Book(isbn=isbn, title=title, price=price, category_id=category_id, author_id=author_id, publisher_id=publisher_id)

    try:
        session.add(book)
        session.commit()
        session.refresh(book)

    except IntegrityError as exc:
        print("Unexpected error : cannot create book")
        session.rollback()
        return None

    return book

# def display_book_publisher(session: Session, book_id:int):
#     stmt = select(Book).options(joinedload(Book.publisher)).where(Book.id == book_id)
#     book = session.execute(stmt).scalar_one_or_none()

#     if book is None:
#         print("No book with this id")
#         return False

#     print(book)
#     print(book.publisher)
#     return True