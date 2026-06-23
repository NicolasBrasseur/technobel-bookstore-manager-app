from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.client_repository import create_client, get_client_by_email
import re

def add_new_client(session:Session, name:str, email:str, country_identifier:str):
    client = get_client_by_email(session, email)
    if client :
        print("Error: A client account with the same email already exists")
        return client
    
    if not re.match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        print("Error: Incorrect email format")
        return None
    
    
    try:
        client = create_client(session, name, email, country_identifier)
        session.commit()
        session.refresh(client)
    except IntegrityError:
        print(f"Unexpected error while creating new client account \"{name}\"")
        session.rollback()
    
    return client