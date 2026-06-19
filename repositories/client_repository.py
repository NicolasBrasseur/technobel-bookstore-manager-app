from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.client import Client

def create_client(session: Session, name: str, country_identifier: str):
    client = Client(session=session, name=name, country_identifier=country_identifier)

    try:
        session.add(client)
        session.commit()
        session.refresh(client)

    except IntegrityError as exc:
        print("Unexpected error : cannot create client")
        session.rollback()
        return None

    return client