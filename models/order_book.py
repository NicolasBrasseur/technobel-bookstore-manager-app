from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class OrderBook(Base):
    __tablename__ = "order_book"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("purchase_order.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)

    def __repr__(self):
        return f"Order-book({self.id}) : quantity = {self.quantity}"