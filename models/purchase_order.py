from database.database import Base
from sqlalchemy import Identity, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from enum import Enum
import datetime

if TYPE_CHECKING:
    from order_book import OrderBook
    from bookstore import Bookstore
    from distributor import Distributor

class Status(Enum):
    PENDING = "Pending payment"
    PROCESSING = "Processing"
    PACKAGED = "Packaged, awaiting shipment"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"


class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    status: Mapped[Status] = mapped_column(nullable=False, default=Status.PENDING)
    total_price: Mapped[float] = mapped_column(nullable=True)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now())
    bookstore_id: Mapped[int] = mapped_column(ForeignKey("bookstore.id"), nullable=False)
    bookstore: Mapped[Bookstore] = relationship("Bookstore", back_populates="orders", uselist=False)
    distributor_id: Mapped[int] = mapped_column(ForeignKey("distributor.id"), nullable=False)
    distributor: Mapped[Distributor] = relationship("Distributor", back_populates="orders", uselist=False)

    order_books: Mapped[OrderBook] = relationship("OrderBook", back_populates="order")

    def __repr__(self):
        return f"Purchase order({self.id}) : status = {self.status.value}, total_price = {self.total_price}, order_date = {self.order_date}"