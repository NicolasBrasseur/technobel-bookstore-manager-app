from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.publisher import Publisher

def create_publisher(session: Session, name: str):
    publisher = Publisher(name=name)
    session.add(publisher)
    return publisher

def get_publisher_by_name(session:Session, name:str):
    stmt = select(Publisher).where(Publisher.name == name)
    publisher = session.execute(stmt).scalar_one_or_none()
    return publisher

def get_publisher_by_id(session:Session, publisher_id:int):
    stmt = select(Publisher).where(Publisher.id == publisher_id)
    publisher = session.execute(stmt).scalar_one_or_none()
    return publisher