from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.bookstore import Bookstore

def create_bookstore(session: Session, name: str, country_identifier: str):
    bookstore = Bookstore(session=session, name=name, country_identifier=country_identifier)

    try:
        session.add(bookstore)
        session.commit()
        session.refresh(bookstore)

    except IntegrityError as exc:
        print("Unexpected error : cannot create bookstore")
        session.rollback()
        return None

    return bookstore