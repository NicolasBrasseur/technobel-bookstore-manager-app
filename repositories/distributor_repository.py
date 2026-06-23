from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.distributor import Distributor

def create_distributor(session: Session, name:str, operating_country_identifier:str):
    distributor = Distributor(session=session, name=name, operating_country_identifier=operating_country_identifier)
    session.add(distributor)
    return distributor

def get_distributor_by_name_and_country(session:Session, name:str, operating_country_identifier:str):
    stmt = select(Distributor).where(and_(Distributor.name == name, Distributor.operating_country_identifier == operating_country_identifier))
    distributor = session.execute(stmt).scalar_one_or_none()
    return distributor