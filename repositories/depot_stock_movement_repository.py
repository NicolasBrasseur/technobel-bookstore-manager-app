from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from models.depot_stock_movement import DepotStockMovement

if TYPE_CHECKING:
    import datetime

def create_depot_stock_movement(session: Session, quantity:int, date: datetime.datetime, comment:str, depot_id:int):
    depot_stock_movement = DepotStockMovement(quantity=quantity, date=date, comment=comment, depot_id=depot_id)
    session.add(depot_stock_movement)
    return depot_stock_movement