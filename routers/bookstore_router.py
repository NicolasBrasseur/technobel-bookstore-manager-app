from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from services.bookstore_service import add_new_bookstore, display_all_bookstore_having_book
from schemas.bookstore_schema import BookstoreCreate, BookstoreResponse


router = APIRouter(prefix="/bookstores", tags=["Bookstores"])


@router.post("/", response_model=BookstoreResponse)
def create_bookstore(bookstore: BookstoreCreate, session: Session = Depends(get_db)):
    try: return add_new_bookstore(session, bookstore.name, bookstore.country_identifier)
    except ValueError as e: raise HTTPException(status_code=409, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))


@router.get("/book/{book_isbn}/{country_identifier}")
def get_bookstores(book_isbn: int, country_identifier: str, session: Session = Depends(get_db)):
    try: return display_all_bookstore_having_book(session, book_isbn, country_identifier)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))