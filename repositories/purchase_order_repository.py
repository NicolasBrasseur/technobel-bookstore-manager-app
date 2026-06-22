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