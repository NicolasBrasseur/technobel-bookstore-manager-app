from database.database import Base
from sqlalchemy import Identity, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class DepotStockMovement(Base):
    __tablename__ = "depot_stock_movement"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now())
    comment: Mapped[str] = mapped_column(String(200), nullable=True)
    depot_id: Mapped[int] = mapped_column(ForeignKey("depot.id"), nullable=False)

    def __repr__(self):
        return f"Depot stock movement({self.id}) : quantity = {self.quantity}, date = {self.date}, comment = {self.comment}"