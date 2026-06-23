from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from models.purchase_order import PurchaseOrder

if TYPE_CHECKING:
    from models.purchase_order import Status
    import datetime

def create_purchase_order(session: Session, status:Status, total_price:int, order_date:datetime.datetime, bookstore_id:int, distributor_id:int):
    purchase_order = PurchaseOrder(session=session, status=status, total_price=total_price, order_date=order_date, bookstore_id=bookstore_id, distributor_id=distributor_id)
    session.add(purchase_order)
    return purchase_order

def display_all_orders_of_distributor(session:Session, distributor_id:int):
    pass

def display_all_orders_of_bookstore(session:Session, bookstore_id:int):
    pass

def add_book_to_order(session:Session, bookstore_id:int, book_id:int, quantity:int):
    pass

def remove_book_from_order(session:Session, bookstore_id:int, book_id:int, quantity:int):
    pass

def validate_order(session:Session, bookstore_id:int):
    pass

def cancel_order(session:Session, bookstore_id:int):
    pass

def change_order_status(session:Session, distibutor_id:int, bookstore_id:int): # Country = country du distributor
    pass