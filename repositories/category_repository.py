from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.category import Category

def create_category(session: Session, name: str):
    category = Category(name=name)
    session.add(category)
    return category

def get_category_by_name(session:Session, name:str):
    stmt = select(Category).where(Category.name == name)
    category = session.execute(stmt).scalar_one_or_none()
    return category