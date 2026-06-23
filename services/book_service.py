from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.book_repository import create_book, get_book_by_isbn, get_all_books, get_all_books_of_author, get_all_books_of_bookstore, get_all_books_of_category, get_all_books_of_publisher, get_book_by_sales
from repositories.category_repository import create_category, get_category_by_name
from repositories.publisher_repository import get_publisher_by_id
from repositories.author_repository import get_author_by_name_and_country
from repositories.country_repository import get_all_countries
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from models.country import Country

def add_new_book(session:Session, isbn:int, title:str, price:float, publication_date:datetime.datetime, category_name:str, author_name:str, author_country_identifier:str, publisher_id:int):
    book = get_book_by_isbn(session, isbn)
    if book :
        print("Error: A book with the same ISBN already exists")
        return book
    
    publisher = get_publisher_by_id(session, publisher_id)
    if not publisher:
        print("Error: You are not logged in as a valid publisher, create a new publisher entry and login to this account first")
        return None
        
    author = get_author_by_name_and_country(session, author_name, author_country_identifier)
    if not author:
        print("Error: No author with this name and country has been found in the database, add this author first")
        return None

    category = get_category_by_name(session, category_name)
    if not category:
        category = create_category(session, category_name)
        print(f"Category {category_name} didn't exist in the database and has been added")
    
    book = create_book(session, isbn, title, price, publication_date, category.id, author.id, publisher_id)
    try:
        session.commit()
        session.refresh(book)
        session.refresh(category)
    except IntegrityError:
        print(f"Unexpected error while adding new book \"{title}\" or creating new category \"{category_name}\"")
        session.rollback()
    
    return book


def display_all_books(session:Session):
    books = get_all_books(session)

    if not books:
        print("There are no elements in the database with the specified conditions")
        return None

    for book in books:
        print(f"● {book}")
        print(f"↪ Category : {book.category}")
        print(f"↪ Author : {book.author}")
        print(f"↪ Publisher : {book.publisher}")
    
    return books


def display_all_books_of_author(session:Session, author_name:str):
    books = get_all_books_of_author(session, author_name)

    if not books:
        print("There are no elements in the database with the specified conditions")
        return None

    for book in books:
        print(f"● {book}")
        print(f"↪ Category : {book.category}")
        print(f"↪ Publisher : {book.publisher}")

    return books


def display_all_books_of_publisher(session:Session, publisher_name:str):
    books = get_all_books_of_publisher(session, publisher_name)

    if not books:
        print("There are no elements in the database with the specified conditions")
        return None

    for book in books:
        print(f"● {book}")
        print(f"↪ Category : {book.category}")
        print(f"↪ Author : {book.author}")

    return books


def display_all_books_of_category(session:Session, category_name):
    books = get_all_books_of_category(session, category_name)

    if not books:
        print("There are no elements in the database with the specified conditions")
        return None

    for book in books:
        print(f"● {book}")
        print(f"↪ Author : {book.author}")
        print(f"↪ Publisher : {book.publisher}")

    return books


def display_all_books_of_bookstore(session:Session, bookstore_name:str, country_identification:str):
    books = get_all_books_of_bookstore(session, bookstore_name, country_identification)

    if not books:
        print("There are no elements in the database with the specified conditions")
        return None

    for book, quantity in books:
        print(f"● {book} ⟫ [ quantity = {quantity} ]")
        print(f"↪ Category : {book.category}")
        print(f"↪ Author : {book.author}")
        print(f"↪ Publisher : {book.publisher}")

    return books

def display_all_book_prices_in_countries(session:Session, book_isbn):
    book = get_book_by_isbn(session, book_isbn)
    if not book:
        print("Error: This book ISBN is not linked to any book in the database")
        return None
    
    countries = get_all_countries(session)
    if not countries:
        print("There are no country saved in the database")
        return None
    
    prices_with_taxes: list[Country, float] = []
    
    print(f"Book base price (taxes not included) : {book.price}")
    for coutry in countries:
        price = book.price * (1 + coutry.vat / 100)
        prices_with_taxes.append((coutry, price))
    
    prices_with_taxes.sort(key= lambda x : x[1])

    for price in prices_with_taxes:
        print(f"Price in {price[0].name} ({price[0].vat}% taxes included) : {price[1]}")

    return prices_with_taxes

def display_book_by_sales(session:Session):
    books = get_book_by_sales(session)

    if not books:
        print("There are no book in the database")
        return None
    
    for i, (book, sales) in enumerate(books):
        print(f"N°{i+1} : {book} ⟫ [ number of sales : {sales} ]")

    