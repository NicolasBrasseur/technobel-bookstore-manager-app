from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.author_schema import AuthorCreate, AuthorResponse
from services.author_service import add_new_author

router = APIRouter(
    prefix="/author",
    tags=["Author"]
)


@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=201
)
def create_author(
    author: AuthorCreate,
    session: Session = Depends(get_db)
):
    try:
        return add_new_author(
            session,
            author.name,
            author.country_identifier
        )

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )