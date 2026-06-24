from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.book_schema import BookCreate, BookResponse

from services.book_service import add_new_book, display_all_books, display_all_books_of_author, display_all_books_of_publisher, display_all_books_of_category, display_all_books_of_bookstore, display_all_book_prices_in_countries, display_book_by_sales


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, session: Session = Depends(get_db)):
    try: return add_new_book(session, book.isbn, book.title, book.price, book.publication_date, book.category_name, book.author_name, book.author_country_identifier, book.publisher_id)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[BookResponse])
def get_books(session: Session = Depends(get_db)):
    return display_all_books(session)


@router.get("/author/{author_name}", response_model=list[BookResponse])
def get_books_by_author(author_name: str, session: Session = Depends(get_db)):
    try: return display_all_books_of_author(session, author_name)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.get("/publisher/{publisher_name}", response_model=list[BookResponse])
def get_books_by_publisher(publisher_name: str, session: Session = Depends(get_db)):
    try: return display_all_books_of_publisher(session, publisher_name)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.get("/category/{category_name}", response_model=list[BookResponse])
def get_books_by_category(category_name: str, session: Session = Depends(get_db)):
    try: return display_all_books_of_category(session, category_name)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.get("/bookstore/{bookstore_name}/{country_identifier}", response_model=list[BookResponse])
def get_books_by_bookstore(bookstore_name: str, country_identifier: str, session: Session = Depends(get_db)):
    try: return display_all_books_of_bookstore(session, bookstore_name, country_identifier)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.get("/prices/{isbn}")
def get_prices(isbn: int, session: Session = Depends(get_db)):
    try: return display_all_book_prices_in_countries(session, isbn)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.get("/sales")
def get_sales(session: Session = Depends(get_db)):
    try: return display_book_by_sales(session)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))