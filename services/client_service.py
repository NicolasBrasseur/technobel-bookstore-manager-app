from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.client_repository import create_client, get_client_by_email
import re


def add_new_client(session: Session, name: str, email: str, country_identifier: str):

    if get_client_by_email(session, email):
        raise ValueError(f"Client with email '{email}' already exists")

    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        raise ValueError("Invalid email format")

    try:
        client = create_client(session, name, email, country_identifier)
        session.commit()
        session.refresh(client)
        return client

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating client '{name}'")