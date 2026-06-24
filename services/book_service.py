from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import datetime

from repositories.book_repository import create_book, get_book_by_isbn, get_all_books, get_all_books_of_author, get_all_books_of_bookstore, get_all_books_of_category, get_all_books_of_publisher, get_book_by_sales
from repositories.category_repository import create_category, get_category_by_name
from repositories.publisher_repository import get_publisher_by_id
from repositories.author_repository import get_author_by_name_and_country
from repositories.country_repository import get_all_countries


def add_new_book(session: Session, isbn: int, title: str, price: float, publication_date: datetime.datetime, category_name: str, author_name: str, author_country_identifier: str, publisher_id: int):

    if get_book_by_isbn(session, isbn): raise ValueError(f"Book with ISBN {isbn} already exists")

    publisher = get_publisher_by_id(session, publisher_id)
    if not publisher: raise ValueError("Publisher not found")

    author = get_author_by_name_and_country(session, author_name, author_country_identifier)
    if not author: raise ValueError("Author not found")

    category = get_category_by_name(session, category_name)
    if not category: category = create_category(session, category_name)

    try:
        book = create_book(session, isbn, title, price, publication_date, category.id, author.id, publisher_id)
        session.commit()
        session.refresh(book)
        return book

    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Error while creating book '{title}'")


def display_all_books(session: Session):
    return get_all_books(session)


def display_all_books_of_author(session: Session, author_name: str):
    books = get_all_books_of_author(session, author_name)
    if not books: raise ValueError("No books found for this author")
    return books


def display_all_books_of_publisher(session: Session, publisher_name: str):
    books = get_all_books_of_publisher(session, publisher_name)
    if not books: raise ValueError("No books found for this publisher")
    return books


def display_all_books_of_category(session: Session, category_name: str):
    books = get_all_books_of_category(session, category_name)
    if not books: raise ValueError("No books found for this category")
    return books


def display_all_books_of_bookstore(session: Session, bookstore_name: str, country_identifier: str):
    books = get_all_books_of_bookstore(session, bookstore_name, country_identifier)
    if not books: raise ValueError("No books found for this bookstore")
    return books


def display_all_book_prices_in_countries(session: Session, book_isbn: int):

    book = get_book_by_isbn(session, book_isbn)
    if not book: raise ValueError("Book not found")

    countries = get_all_countries(session)
    if not countries: raise ValueError("No countries found")

    result = []
    for country in countries:
        price = book.price * (1 + country.vat / 100)
        result.append({"country": country.name, "vat": country.vat, "price": price})

    result.sort(key=lambda x: x["price"])
    return {"base_price": book.price, "prices": result}


def display_book_by_sales(session: Session):
    books = get_book_by_sales(session)
    if not books: raise ValueError("No books found")
    return [{"book": book, "sales": sales} for book, sales in books]

    