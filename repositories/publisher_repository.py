from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.publisher import Publisher

def create_publisher(session: Session, name: str):
    publisher = Publisher(name=name)
    session.add(publisher)
    return publisher

def get_publisher_by_name(session:Session, name:str):
    pass