from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import datetime

from models.purchase_order import Status

from repositories.purchase_order_repository import create_purchase, get_all_purchases_of_bookstore, get_all_purchases_of_distributor, get_purchase_by_distributor_id_status_and_bookstore_id, get_purchase_by_distributor_status_and_bookstore
from repositories.order_book_repository import get_order_book_by_book_and_status, create_order_book, get_orders_book_by_purchase_order_id
from repositories.distributor_repository import get_distributor_with_book_stock, get_distributor_by_id
from repositories.book_repository import get_book_by_isbn
from repositories.bookstore_repository import get_bookstore_by_id
from repositories.country_repository import get_country_by_identifier
from repositories.depot_repository import get_depot, create_depot
from repositories.bookstore_shelf_repository import get_bookstore_shelf, create_bookstore_shelf
from repositories.depot_stock_movement_repository import create_depot_stock_movement
from repositories.shelf_stock_movement_repository import create_shelf_stock_movement


def display_all_purchases_of_bookstore(session: Session, bookstore_id: int):
    purchases = get_all_purchases_of_bookstore(session, bookstore_id)
    if not purchases: raise ValueError("No purchase orders found for this bookstore")
    return purchases


def display_all_purchases_of_distributor(session: Session, distributor_id: int):
    purchases = get_all_purchases_of_distributor(session, distributor_id)
    if not purchases: raise ValueError("No purchase orders found for this distributor")
    return purchases


def add_book_to_purchase_order(session: Session, book_isbn: int, bookstore_id: int, quantity: int):

    book = get_book_by_isbn(session, book_isbn)
    if not book: raise ValueError("Book not found")

    distributor, stock_qty = get_distributor_with_book_stock(session, book_isbn)
    if not distributor: raise ValueError("No distributor has stock for this book")

    if stock_qty < quantity:
        pass  # volontaire : on laisse passer mais stock insuffisant

    purchase = get_purchase_by_distributor_id_status_and_bookstore_id(session, distributor.id, bookstore_id, Status.PENDING)
    if not purchase:
        purchase = create_purchase(session, Status.PENDING, 0, datetime.datetime.now(), bookstore_id, distributor.id)

    order = get_order_book_by_book_and_status(session, book_isbn, bookstore_id, Status.PENDING)
    if not order:
        order = create_order_book(session, quantity, purchase.id, book.id)
    else:
        order.quantity += quantity

    try:
        session.commit()
        session.refresh(purchase)
        session.refresh(order)
        return order

    except IntegrityError:
        session.rollback()
        raise RuntimeError("Error while adding book to purchase order")


def remove_book_from_purchase_order(session: Session, book_isbn: int, bookstore_id: int, quantity: int):

    book = get_book_by_isbn(session, book_isbn)
    if not book: raise ValueError("Book not found")

    order = get_order_book_by_book_and_status(session, book_isbn, bookstore_id, Status.PENDING)
    if not order: raise ValueError("No pending order found")

    order.quantity = max(0, order.quantity - quantity)

    if order.quantity == 0:
        session.delete(order)

    session.commit()
    return order


def validate_all_purchase_orders(session: Session, bookstore_id: int):

    purchases = get_all_purchases_of_bookstore(session, bookstore_id)
    if not purchases: raise ValueError("No purchase orders found")

    bookstore = get_bookstore_by_id(session, bookstore_id)
    if not bookstore: raise ValueError("Bookstore not found")

    validated = []

    for purchase in purchases:
        if purchase.status == Status.PENDING:
            validate_purchase_order(session, purchase, bookstore.country_identifier)
            validated.append(purchase)

    if not validated: raise ValueError("No purchase orders to validate")

    session.commit()
    return validated


def validate_purchase_order(session: Session, purchase_order, country_identifier: str):

    orders = get_orders_book_by_purchase_order_id(session, purchase_order.id)
    if not orders:
        session.delete(purchase_order)
        session.commit()
        return None

    country = get_country_by_identifier(session, country_identifier)

    total_price = sum(order.book.price * (1 + country.vat / 100) * order.quantity for order in orders)

    purchase_order.total_price = total_price
    purchase_order.status = Status.PROCESSING

    return purchase_order


def cancel_all_purchase_orders(session: Session, bookstore_id: int):

    purchases = get_all_purchases_of_bookstore(session, bookstore_id)
    if not purchases: raise ValueError("No purchase orders found")

    for purchase in purchases:
        purchase.status = Status.CANCELLED

    session.commit()
    return purchases


def packaged_purchase_order_of_bookstore(session: Session, distributor_id: int, bookstore_name: str):

    purchases = get_purchase_by_distributor_status_and_bookstore(session, distributor_id, bookstore_name, Status.PROCESSING)
    if not purchases: raise ValueError("No purchase orders ready for packaging")

    for purchase in purchases:
        for order in purchase.order_books:

            depot = get_depot(session, distributor_id, order.book.id)
            if not depot or depot.stock_quantity < order.quantity:
                session.rollback()
                raise ValueError("Insufficient depot stock")

            depot.stock_quantity -= order.quantity

            create_depot_stock_movement(session, order.quantity, datetime.datetime.now(), f"Purchase {purchase.id}", depot.id)

        purchase.status = Status.PACKAGED
        session.commit()

    return purchases


def ship_purchase_order(session: Session, distributor_id: int, bookstore_name: str):

    purchases = get_purchase_by_distributor_status_and_bookstore(session, distributor_id, bookstore_name, Status.PACKAGED)
    if not purchases: raise ValueError("No purchase orders to ship")

    for purchase in purchases:
        purchase.status = Status.SHIPPED

    session.commit()
    return purchases


def deliver_purchase_order(session: Session, distributor_id: int, bookstore_name: str):

    purchases = get_purchase_by_distributor_status_and_bookstore(session, distributor_id, bookstore_name, Status.SHIPPED)
    if not purchases: raise ValueError("No purchase orders to deliver")

    distributor = get_distributor_by_id(session, distributor_id)
    if not distributor: raise ValueError("Distributor not found")

    for purchase in purchases:
        for order in purchase.order_books:

            shelf = get_bookstore_shelf(session, distributor.id, order.book.id)

            if not shelf:
                shelf = create_bookstore_shelf(session, order.quantity, distributor.id, order.book.id)
            else:
                shelf.quantity += order.quantity

            create_shelf_stock_movement(session, order.quantity, datetime.datetime.now(), f"Delivery {purchase.id}", shelf.id)

        purchase.status = Status.DELIVERED
        session.commit()

    return purchases


def buy_book(session: Session, bookstore_id: int, book_isbn: int, quantity: int):

    book = get_book_by_isbn(session, book_isbn)
    if not book: raise ValueError("Book not found")

    shelf = get_bookstore_shelf(session, bookstore_id, book.id)
    if not shelf: raise ValueError("Book not in stock")

    if shelf.quantity < quantity: raise ValueError("Insufficient stock")

    shelf.quantity -= quantity

    create_shelf_stock_movement(session, -quantity, datetime.datetime.now(), "Customer purchase", shelf.id)

    session.commit()
    return shelf


def add_stock(session: Session, distributor_id: int, book_isbn: int, quantity: int):

    book = get_book_by_isbn(session, book_isbn)
    if not book: raise ValueError("Book not found")

    depot = get_depot(session, distributor_id, book.id)

    if not depot:
        depot = create_depot(session, quantity, distributor_id, book.id)
    else:
        depot.stock_quantity += quantity

    create_depot_stock_movement(session, quantity, datetime.datetime.now(), "Stock update", depot.id)

    session.commit()
    return depot

    
