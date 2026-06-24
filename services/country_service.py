from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.country_repository import create_country, get_country_by_identifier


def add_new_country(session: Session, identifier: str, name: str, vat: float):

    if get_country_by_identifier(session, identifier):
        raise ValueError(f"Country '{identifier}' already exists")

    try:
        country = create_country(session, identifier, name, vat)
        session.commit()
        session.refresh(country)
        return country

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating country '{name}'")