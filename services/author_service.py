from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories.author_repository import (
    create_author,
    get_author_by_name_and_country
)


def add_new_author(session: Session, name: str, country_identifier: str):

    author = get_author_by_name_and_country(
        session,
        name,
        country_identifier
    )

    if author:
        raise ValueError(
            f'Author "{name}" already exists in country "{country_identifier}"'
        )

    try:
        author = create_author(session, name, country_identifier)

        session.commit()
        session.refresh(author)

        return author

    except IntegrityError:
        session.rollback()
        raise RuntimeError(
            f'Unexpected error while creating author "{name}"'
        )