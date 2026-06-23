from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.purchase_order_repository import create_purchase, get_all_purchases_of_bookstore, get_all_purchases_of_distributor, get_purchase_by_distributor_id_status_and_bookstore_id
from repositories.order_book_repository import get_order_book_by_book_and_status, create_order_book
from repositories.distributor_repository import get_distributor_with_book_stock
from repositories.book_repository import get_book_by_isbn
from models.purchase_order import Status
import datetime

def display_all_purchases_of_bookstore(session:Session, bookstore_id:int):
    purchases = get_all_purchases_of_bookstore(session, bookstore_id)
    if not purchases:
        print("There are no purchases order")
        return None
    
    for purchase in purchases:
        print(purchase)

    return purchases

def display_all_purchases_of_distributor(session:Session, distributor_id:int):
    purchases = get_all_purchases_of_distributor(session, distributor_id)
    if not purchases:
        print("There are no purchases order")
        return None
    
    for purchase in purchases:
        print(purchase)

    return purchases

def add_book_to_purchase_order(session:Session, book_isbn:int, bookstore_id:int, quantity:int):

    book = get_book_by_isbn(session, book_isbn)
    if not book:
        print("This book is not saved in the database")
        return None

    order = get_order_book_by_book_and_status(session, book_isbn, bookstore_id, Status.PENDING)
    if not order:
        distributor, distributor_stock_quantity = get_distributor_with_book_stock(session, book_isbn)
        if not distributor:
            print("There is no distributor with stock for this book")
            return None
        
        if distributor_stock_quantity < quantity:
            print(f"!! : Distributor currently don't have sufficient stock for this book ({distributor_stock_quantity}/{quantity}) but order is still proceeding")

        purchase = get_purchase_by_distributor_id_status_and_bookstore_id(session, distributor.id, bookstore_id, Status.PENDING)
        if not purchase:
            purchase = create_purchase(session, Status.PENDING, 0, datetime.datetime.now(), bookstore_id, distributor.id)
            print(f"New purchase order created with {distributor.name}")
        
        order = create_order_book(session, quantity, purchase.id, book.id)
    else:
        order.quantity += quantity

    try:
        session.commit()
        session.refresh(purchase)
        session.commit(order)
    except IntegrityError:
        print("Unexpected error while adding book to purchase")
        return None
    
    return order