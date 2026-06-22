from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.depot import Depot

def create_depot(session: Session, stock_quantity:int, distibutor_id:int, book_id:int):
    depot = Depot(session=session, stock_quantity=stock_quantity, distibutor_id=distibutor_id, book_id=book_id)

    try:
        session.add(depot)
        session.commit()
        session.refresh(depot)

    except IntegrityError as exc:
        print("Unexpected error : cannot create depot")
        session.rollback()
        return None

    return depot

def add_stock(session:Session, distributor_id:int, book_id:int, quantity:int):
    pass