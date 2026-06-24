from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.distributor_repository import create_distributor, get_distributor_by_name_and_country


def add_new_distributor(session: Session, name: str, operating_country_identifier: str):

    if get_distributor_by_name_and_country(session, name, operating_country_identifier):
        raise ValueError(f"Distributor '{name}' already exists in country '{operating_country_identifier}'")

    try:
        distributor = create_distributor(session, name, operating_country_identifier)
        session.commit()
        session.refresh(distributor)
        return distributor

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating distributor '{name}'")