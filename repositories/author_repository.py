from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.author import Author

def create_author(session: Session, name: str, country_identifier: str):
    author = Author(name=name, country_identifier=country_identifier)
    session.add(author)
    return author

def get_author_by_name_and_country(session:Session, name:str, country_identifier:str):
    stmt = select(Author).where(and_(Author.name == name, Author.country_identifier == country_identifier))
    author = session.execute(stmt).scalar_one_or_none()

    return author