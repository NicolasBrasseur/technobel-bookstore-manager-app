from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.distributor_repository import create_distributor, get_distributor_by_name_and_country

def add_new_author(session:Session, name:str, operating_country_identifier:str):
    distributor = get_distributor_by_name_and_country(session, name, operating_country_identifier)
    if distributor :
        print("Error: A distributor with the same name already exists for the specified country")
        return distributor
    
    try:
        distributor = create_distributor(session, name, operating_country_identifier)
        session.commit()
        session.refresh(distributor)
    except IntegrityError:
        print(f"Unexpected error while creating new distributor \"{name}\"")
        session.rollback()
    
    return distributor