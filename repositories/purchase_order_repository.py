from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING
import datetime

from models.purchase_order import PurchaseOrder
from models.distributor import Distributor
from models.bookstore import Bookstore

if TYPE_CHECKING:
    from models.purchase_order import Status

def create_purchase(session: Session, status:Status, total_price:int, order_date:datetime.datetime, bookstore_id:int, distributor_id:int):
    purchase_order = PurchaseOrder(status=status, total_price=total_price, order_date=order_date, bookstore_id=bookstore_id, distributor_id=distributor_id)
    session.add(purchase_order)
    return purchase_order

def get_all_purchases_of_distributor(session:Session, distributor_id:int):
    stmt = select(PurchaseOrder).where(PurchaseOrder.distributor_id == distributor_id)
    orders = session.execute(stmt).scalars().all()
    return orders

def get_all_purchases_of_bookstore(session:Session, bookstore_id:int):
    stmt = select(PurchaseOrder).where(PurchaseOrder.bookstore_id == bookstore_id)
    orders = session.execute(stmt).scalars().all()
    return orders

def get_purchases_by_bookstore_and_status(session:Session, bookstore_id:int, status:Status):
    stmt = select(PurchaseOrder).where(and_(PurchaseOrder.bookstore_id == bookstore_id, PurchaseOrder.status == status))
    orders = session.execute(stmt).scalars().all()
    return orders

def get_purchases_by_distributor_and_status(session:Session, distibutor_id:int, status:Status):
    stmt = select(PurchaseOrder).where(and_(PurchaseOrder.distributor_id == distibutor_id, PurchaseOrder.status == status))
    orders = session.execute(stmt).scalars().all()
    return orders

def get_purchase_by_distributor_status_and_bookstore(session:Session, distributor_id:int, bookstore_name:str, status:Status):
    stmt = (select(PurchaseOrder).distinct().join(PurchaseOrder.bookstore).join(PurchaseOrder.distributor)
            .where(PurchaseOrder.distributor_id == distributor_id, PurchaseOrder.status == status, Bookstore.country_identifier == Distributor.operating_country_identifier, Bookstore.name == bookstore_name)
    )
    orders = session.execute(stmt).scalars().all()
    return orders

