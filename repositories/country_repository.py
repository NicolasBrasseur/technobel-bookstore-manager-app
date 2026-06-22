from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.country import Country

def create_country(session: Session, identifier: str, name: str, vat: float):
    country = Country(session=session, identifier=identifier, name=name, vat=vat)

    try:
        session.add(country)
        session.commit()
        session.refresh(country)

    except IntegrityError as exc:
        print("Unexpected error : cannot create country")
        session.rollback()
        return None

    return country

def get_country_by_identifier(session:Session, identifier:str):
    pass