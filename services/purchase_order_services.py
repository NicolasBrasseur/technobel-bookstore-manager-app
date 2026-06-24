from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.purchase_order_repository import create_purchase, get_all_purchases_of_bookstore, get_all_purchases_of_distributor, get_purchase_by_distributor_id_status_and_bookstore_id, get_purchase_by_distributor_status_and_bookstore
from repositories.order_book_repository import get_order_book_by_book_and_status, create_order_book, get_orders_book_by_purchase_order_id
from repositories.distributor_repository import get_distributor_with_book_stock, get_distributor_by_id
from repositories.book_repository import get_book_by_isbn, get_book_by_id
from repositories.bookstore_repository import get_bookstore_by_id
from repositories.country_repository import get_country_by_identifier
from repositories.depot_repository import get_depot, create_depot
from repositories.bookstore_shelf_repository import get_bookstore_shelf, create_bookstore_shelf
from repositories.depot_stock_movement_repository import create_depot_stock_movement
from repositories.shelf_stock_movement_repository import create_shelf_stock_movement
from models.purchase_order import Status
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from models.purchase_order import PurchaseOrder

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

    order = get_order_book_by_book_and_status(session, book_isbn, bookstore_id, Status.PENDING)
    if not order:
        
        order = create_order_book(session, quantity, purchase.id, book.id)
    else:
        order.quantity += quantity

    print(purchase)

    try:
        session.commit()
        session.refresh(purchase)
        session.refresh(order)
    except IntegrityError:
        print("Unexpected error while adding book to purchase")
        return None
    
    return order

def remove_book_from_purchase_order(session:Session, book_isbn:int, bookstore_id:int, quantity:int):
    print(f"Quantity : {quantity}")
    book = get_book_by_isbn(session, book_isbn)
    if not book:
        ("This book is not saved in the database")
        return None
    
    order = get_order_book_by_book_and_status(session, book_isbn, bookstore_id, Status.PENDING)
    if not order:
        print("No pending order found with this book, the order either has a another status or don't exist")
        return None
    
    print(f"Previous quantity : {order.quantity}")
    order.quantity = max(0, order.quantity - quantity)
    print(f"New order quantity : {order.quantity}")

    if order.quantity <= 0:
        print("Deleting empty order")
        session.delete(order)
        session.commit()
        return None
    
    session.commit()

    return order

def validate_all_purchase_orders(session:Session, bookstore_id:int):
    purchases = get_all_purchases_of_distributor(session, bookstore_id)
    if not purchases:
        print("There are no purchases associated with this bookstore")
        return None
    
    validated_purchases = []
    bookstore = get_bookstore_by_id(session, bookstore_id)
    if not bookstore:
        print("You are not logged to a bookstore account")
        return None

    country_identifier = bookstore.country_identifier
    
    for purchase in purchases:
        if purchase.status == Status.PENDING:
            validate_purchase_order(session, purchase, country_identifier)
            validated_purchases.append(purchase)
    
    if not validated_purchases:
        print("There is no purchase that need to be validated")
        return None
    
    session.commit()
    return validated_purchases

def validate_purchase_order(session:Session, purchase_order:PurchaseOrder, operating_country_identifier:str):
    orders = get_orders_book_by_purchase_order_id(session, purchase_order.id)
    if not orders:
        print("Purchase order is empty, deleting")
        session.delete(purchase_order)
        session.commit()
        return None
    
    total_price = 0
    country = get_country_by_identifier(session, operating_country_identifier)
    for order in orders:
        total_price += order.book.price * (1 + country.vat/100) * order.quantity
    
    purchase_order.total_price = total_price
    purchase_order.status = Status.PROCESSING
    return purchase_order

def cancel_all_purchase_orders(session:Session, bookstore_id:int):
    purchases = get_all_purchases_of_bookstore(session, bookstore_id)
    if not purchases:
        print("There are no purchase to cancel")
        return None
    
    for purchase in purchases:
        purchase.status = Status.CANCELLED
        print(f"Purchase {purchase.id} cancelled")

    session.commit()
    return purchases

def packaged_purchase_order_of_bookstore(session:Session, distributor_id:str, bookstore_name:str):
    purchases = get_purchase_by_distributor_status_and_bookstore(session, distributor_id, bookstore_name, Status.PROCESSING)
    if not purchases:
        print("No purchase can be packaged at this time")
        return None

    for purchase in purchases:
        for order in purchase.order_books:
            depot = get_depot(session, distributor_id, order.book.id)
            if not depot or depot.stock_quantity < order.quantity:
                print("Not enough book in depot to complete order")
                session.rollback()
                return purchases
            depot.stock_quantity -= order.quantity
            create_depot_stock_movement(session, order.quantity, datetime.datetime.now(), f"Purchase {purchase.id}, order {order.id} for {bookstore_name} : {order.quantity}x {order.book.title}, stock remaining : {depot.stock_quantity}", depot.id)

        purchase.status = Status.PACKAGED
        session.commit()
    return purchases

def ship_purchase_order(session:Session, distributor_id, bookstore_name):
    purchases = get_purchase_by_distributor_status_and_bookstore(session, distributor_id, bookstore_name, Status.PACKAGED)
    if not purchases:
        print("No purchase to ship")
        return None
    
    for purchase in purchases:
        purchase.status = Status.SHIPPED
        session.commit()
    return purchases

def deliver_purchase_order(session:Session, distributor_id, bookstore_name):
    purchases = get_purchase_by_distributor_status_and_bookstore(session, distributor_id, bookstore_name, Status.SHIPPED)
    if not purchases:
        print("No purchase to deliver")
        return None
    
    bookstore = get_distributor_by_id(session, distributor_id)
    country = bookstore.operating_country_identifier

    for purchase in purchases:
        for order in purchase.order_books:
            bookstore_shelf = get_bookstore_shelf(session, bookstore.id, order.book.id)
            if not bookstore_shelf:
                bookstore_shelf = create_bookstore_shelf(session, order.quantity, bookstore.id, order.book.id)
            else:
                bookstore_shelf.quantity += order.quantity
            create_shelf_stock_movement(session, order.quantity, datetime.datetime.now(), f"Purchase {purchase.id}, order {order.id} for {bookstore_name} : {order.quantity}x {order.book.title}, stock remaining : {bookstore_shelf.quantity}", bookstore_shelf.id)
        purchase.status = Status.DELIVERED
        session.commit()
    return purchases

def buy_book(session: Session, bookstore_id: int, book_isbn: int, quantity: int):
    book = get_book_by_isbn(session, book_isbn)
    bookstore_shelf = get_bookstore_shelf(session, bookstore_id, book.id)

    if not bookstore_shelf:
        print("Book not found in bookstore stock")
        return None

    if bookstore_shelf.quantity < quantity:
        print("Not enough stock available")
        return None

    bookstore_shelf.quantity -= quantity
    create_shelf_stock_movement(session,-quantity,datetime.datetime.now(), f"Customer purchase : {quantity}x {bookstore_shelf.book.title}, stock remaining : {bookstore_shelf.quantity}", bookstore_shelf.id)

    session.commit()

    print(f"Purchase completed : {quantity}x {bookstore_shelf.book.title}")
    return bookstore_shelf

def add_stock(session: Session, distributor_id: str, book_isbn: int, quantity: int):
    book = get_book_by_isbn(session, book_isbn)
    depot = get_depot(session, distributor_id, book.id)

    if not depot:
        depot = create_depot(session, quantity, distributor_id, book.id)
        create_depot_stock_movement(session, quantity, datetime.datetime.now(), f"Initial stock creation : {quantity}x {book.title}, stock available : {depot.stock_quantity}", depot.id)

        session.commit()

        print(f"Depot created for book {book.title}")
        return depot

    depot.stock_quantity += quantity
    create_depot_stock_movement(session, quantity, datetime.datetime.now(), f"Stock replenishment : {quantity}x {book.title}, stock available : {depot.stock_quantity}", depot.id)

    session.commit()

    print(f"Stock added : {quantity}x {book.title}")
    return depot

    
