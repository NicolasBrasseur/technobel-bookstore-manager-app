from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.depot import Depot

def create_depot(session: Session, stock_quantity:int, distibutor_id:int, book_id:int):
    depot = Depot(session=session, stock_quantity=stock_quantity, distibutor_id=distibutor_id, book_id=book_id)
    session.add(depot)
    return depot

def get_depot(session:Session, distributor_id:int, book_id:int):
    stmt = select(Depot).where(and_(Depot.distributor_id == distributor_id, Depot.book_id == book_id))
    depot = session.execute(stmt).scalar_one_or_none()
    return depot