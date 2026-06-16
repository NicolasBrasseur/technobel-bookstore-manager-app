from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

class ShelfStockMovement(Base):
    __tablename__ = "shelf_stock_movement"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)

    def __repr__(self):
        return f"Shelf stock movement({self.id}) :"