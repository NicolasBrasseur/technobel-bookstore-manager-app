from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.bookstore_repository import create_bookstore, get_bookstore_by_name_and_country, get_all_bookstore_having_book

def add_new_bookstore(session:Session, name:str, country_identifier:str):
    bookstore = get_bookstore_by_name_and_country(session, name, country_identifier)
    if bookstore :
        print("Error: A bookstore with the same name and country already exists")
        return bookstore
    
    try:
        bookstore = create_bookstore(session, name, country_identifier)
        session.commit()
        session.refresh(bookstore)
    except IntegrityError:
        print(f"Unexpected error while creating new bookstore \"{name}\"")
        session.rollback()
    
    return bookstore

def display_all_bookstore_having_book(session:Session, book_isbn:int, country_identifier:str):
    bookstores = get_all_bookstore_having_book(session, book_isbn, country_identifier)

    if not bookstores:
        print("There is no bookstore that have this book in the specified country")
        return None
    
    for bookstore, quantity in bookstores:
        print(f"{bookstore} ⟫ [ quantity = {quantity} ]")
    
    return bookstores