from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.author_repository import create_author, get_author_by_name_and_country

def add_new_author(session:Session, name:str, country_identifier:str):
    author = get_author_by_name_and_country(session, name, country_identifier)
    if author :
        print("Error: An author with the same name and country already exists")
        return author
    
    try:
        author = create_author(session, name, country_identifier)
        session.commit()
        session.refresh(author)
    except IntegrityError:
        print(f"Unexpected error while creating new author \"{name}\"")
        session.rollback()
    
    return author