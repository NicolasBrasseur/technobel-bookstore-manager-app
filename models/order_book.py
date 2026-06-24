from database.database import Base
from sqlalchemy import Identity, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from purchase_order import PurchaseOrder
    from book import Book

class OrderBook(Base):
    __tablename__ = "order_book"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("purchase_order.id"), nullable=False)
    order: Mapped[PurchaseOrder] = relationship("PurchaseOrder", back_populates="order_books", uselist=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    book: Mapped[Book] = relationship("Book", back_populates="order_books", uselist=False)

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_quantity"),
    )

    def __repr__(self):
        return f"> Order-book({self.id}) : quantity = {self.quantity}"