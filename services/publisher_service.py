from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.publisher_repository import create_publisher, get_publisher_by_name

def add_new_publisher(session:Session, name:str):
    publisher = get_publisher_by_name(session, name)
    if publisher :
        print("Error: A publisher with the same name already exists")
        return publisher
    
    try:
        publisher = create_publisher(session, name)
        session.commit()
        session.refresh(publisher)
    except IntegrityError:
        print(f"Unexpected error while creating new publisher \"{name}\"")
        session.rollback()
    
    return publisher