from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.publisher import Publisher

def create_publisher(session: Session, name: str):
    publisher = Publisher(name=name)

    try:
        session.add(publisher)
        session.commit()
        session.refresh(publisher)
    except IntegrityError:
        print("Unexpected error while creating publisher, possible id conflict")
        session.rollback()
        return None
    
    return publisher


def display_all_publishers(session: Session):
    stmt = select(Publisher)
    publishers = session.execute(stmt).scalars().all()

    for publisher in publishers:
        print(publisher)