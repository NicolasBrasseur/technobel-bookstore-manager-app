from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.country_repository import create_country, get_country_by_identifier

def add_new_country(session:Session, identifier:str, name:str, vat:float):
    country = get_country_by_identifier(session, identifier)
    if country :
        print("Error: A country with the same identifier already exists")
        return country
    
    try:
        country = create_country(session, identifier, name, vat)
        session.commit()
        session.refresh(country)
    except IntegrityError:
        print(f"Unexpected error while creating new country \"{name}\"")
        session.rollback()
    
    return country