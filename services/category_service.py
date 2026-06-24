from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories.category_repository import create_category, get_category_by_name


def add_new_category(session: Session, name: str):

    if get_category_by_name(session, name):
        raise ValueError(f"Category '{name}' already exists")

    try:
        category = create_category(session, name)
        session.commit()
        session.refresh(category)
        return category

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating category '{name}'")