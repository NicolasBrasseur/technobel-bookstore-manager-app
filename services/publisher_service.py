from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.publisher_repository import create_publisher, get_publisher_by_name


def add_new_publisher(session: Session, name: str):

    if get_publisher_by_name(session, name):
        raise ValueError(f"Publisher '{name}' already exists")

    try:
        publisher = create_publisher(session, name)
        session.commit()
        session.refresh(publisher)
        return publisher

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating publisher '{name}'")