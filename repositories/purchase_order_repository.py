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

    try:
        session.add(purchase_order)
        session.commit()
        session.refresh(purchase_order)

    except IntegrityError as exc:
        print("Unexpected error : cannot create purchase order")
        session.rollback()
        return None

    return purchase_order

def display_all_orders_of_distributor(session:Session, distributor_id:int):
    pass

def display_all_orders_of_bookstore(session:Session, bookstore_id:int):
    pass

def add_book_to_order(session:Session, bookstore_id:int, book_id:int, quantity:int):
    pass

def remove_book_from_order(session:Session, bookstore_id:int, book_id:int, quantity:int):
    pass

def validate_order(session:Session, bookstore_id:int): # Ajouter distributor id ou name + country pour ne valider que les commande de ce distributeur ?
    pass

def cancel_order(session:Session, bookstore_id:int):
    pass

def packaged_order(session:Session, distributor_id): # Ajouter bookstore id ou name + country pour ne valider que les commandes de ce libraire ?
    pass