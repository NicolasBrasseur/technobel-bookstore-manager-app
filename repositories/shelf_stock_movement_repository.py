from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from models.shelf_stock_movement import ShelfStockMovement

if TYPE_CHECKING:
    import datetime

def create_shelf_stock_movement(session: Session, quantity:int, date:datetime.datetime, comment:str, bookstore_shelf_id:int):
    shelf_stock_movement = ShelfStockMovement(quantity=quantity, date=date, comment=comment, bookstore_shelf_id=bookstore_shelf_id)
    session.add(shelf_stock_movement)
    return shelf_stock_movement