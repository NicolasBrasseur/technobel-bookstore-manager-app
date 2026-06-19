from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.order_book import OrderBook

def create_order_book(session: Session, quantity: int, order_id: int, book_id: int):
    order_book = OrderBook(session=session, quantity=quantity, order_id=order_id, book_id=book_id)

    try:
        session.add(order_book)
        session.commit()
        session.refresh(order_book)

    except IntegrityError as exc:
        print("Unexpected error : cannot create order book")
        session.rollback()
        return None

    return order_book