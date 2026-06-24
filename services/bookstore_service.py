from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories.bookstore_repository import create_bookstore, get_bookstore_by_name_and_country, get_all_bookstore_having_book


def add_new_bookstore(session: Session, name: str, country_identifier: str):

    if get_bookstore_by_name_and_country(session, name, country_identifier):
        raise ValueError(f"Bookstore '{name}' already exists in country '{country_identifier}'")

    try:
        bookstore = create_bookstore(session, name, country_identifier)
        session.commit()
        session.refresh(bookstore)
        return bookstore

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating bookstore '{name}'")


def display_all_bookstore_having_book(session: Session, book_isbn: int, country_identifier: str):

    bookstores = get_all_bookstore_having_book(session, book_isbn, country_identifier)
    if not bookstores:
        raise ValueError("No bookstore found for this book in this country")

    return bookstores