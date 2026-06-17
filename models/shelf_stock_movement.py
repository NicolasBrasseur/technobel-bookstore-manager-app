from database.database import Base
from sqlalchemy import Identity, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class ShelfStockMovement(Base):
    __tablename__ = "shelf_stock_movement"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    comment: Mapped[str] = mapped_column(String(200), nullable=True)
    bookstore_shelf_id: Mapped[int] = mapped_column(ForeignKey("bookstore_shelf.id"), nullable=False)

    def __repr__(self):
        return f"Shelf stock movement({self.id}) : quantity = {self.quantity}, date = {self.date}, comment = {self.comment}"