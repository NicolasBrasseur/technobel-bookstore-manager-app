from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.distributor import Distributor

def create_distributor(session: Session, name:str, operating_country_identifier:str):
    distributor = Distributor(session=session, name=name, operating_country_identifier=operating_country_identifier)

    try:
        session.add(distributor)
        session.commit()
        session.refresh(distributor)

    except IntegrityError as exc:
        print("Unexpected error : cannot create distributor")
        session.rollback()
        return None

    return distributor