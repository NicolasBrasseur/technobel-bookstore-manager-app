from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.client import Client

def create_client(session: Session, name: str, email:str, country_identifier: str):
    client = Client(name=name, email=email, country_identifier=country_identifier)
    session.add(client)
    return client

def get_client_by_email(session:Session, email:str):
    stmt = select(Client).where(Client.email == email)
    client = session.execute(stmt).scalar_one_or_none()
    return client