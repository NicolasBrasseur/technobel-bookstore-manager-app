from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.country import Country

def create_country(session: Session, identifier: str, name: str, vat: float):
    country = Country(session=session, identifier=identifier, name=name, vat=vat)
    session.add(country)
    return country

def get_country_by_identifier(session:Session, identifier:str):
    stmt = select(Country).where(Country.identifier == identifier)
    country = session.execute(stmt).scalar_one_or_none()
    return country

def get_all(session:Session):
    stmt = select(Country)
    countries = session.execute(stmt).scalars().all()
    return countries