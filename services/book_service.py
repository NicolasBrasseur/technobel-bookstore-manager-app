from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.book_repository import create_book, get_book_by_isbn
from repositories.category_repository import create_category, get_category_by_name
from repositories.publisher_repository import get_publisher_by_id
from repositories.author_repository import get_author_by_name_and_country
import datetime

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