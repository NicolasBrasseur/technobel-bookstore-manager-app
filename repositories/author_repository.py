from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.author import Author

def create_author(session: Session, name: str, country_identifier: str):
    author = Author(session=session, name=name, country_identifier=country_identifier)

    try:
        session.add(author)
        session.commit()
        session.refresh(author)

    except IntegrityError as exc:
        print("Unexpected error : cannot create author")
        session.rollback()
        return None

    return author

def get_author_by_name_and_country(session:Session, name:str, country_identifier:str):
    stmt = select(Author).where(and_(Author.name == name, Author.country_identifier == country_identifier))
    author = session.execute(stmt).scalar_one_or_none()

    return author