from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.category import Category

def create_category(session: Session, name: str):
    category = Category(session=session, name=name)

    try:
        session.add(category)
        session.commit()
        session.refresh(category)

    except IntegrityError as exc:
        print("Unexpected error : cannot create category")
        session.rollback()
        return None

    return category

def get_category_by_name(session:Session, name:str):
    pass