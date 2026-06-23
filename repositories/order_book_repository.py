from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from models.order_book import OrderBook
from models.purchase_order import PurchaseOrder
from models.book import Book

if TYPE_CHECKING:
    from models.purchase_order import Status

def create_order_book(session: Session, quantity: int, order_id: int, book_id: int):
    order_book = OrderBook(session=session, quantity=quantity, order_id=order_id, book_id=book_id)
    session.add(order_book)
    return order_book

def get_order_by_book_and_status(session:Session, book_isbn:int, bookstore_id:int, status:Status):
    stmt = (select(OrderBook).distinct().join(OrderBook.order).join(OrderBook.book)
            .where(PurchaseOrder.bookstore_id == bookstore_id, PurchaseOrder.status == status, Book.isbn == book_isbn)
    )
    orders = session.execute(stmt).scalars().all()
    return orders

def delete_order(session:Session, order):
    session.delete(order)