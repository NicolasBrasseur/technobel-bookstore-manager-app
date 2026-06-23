from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.category_repository import create_category, get_category_by_name

def add_new_category(session:Session, name:str):
    category = get_category_by_name(session, name)
    if category :
        print("Error: A category with the same name already exists")
        return category
    
    try:
        category = create_category(session, name)
        session.commit()
        session.refresh(category)
    except IntegrityError:
        print(f"Unexpected error while creating new category \"{name}\"")
        session.rollback()
    
    return category