from database.database import Base
from sqlalchemy import Identity, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from depot_stock_movement import DepotStockMovement
    from distributor import Distributor
    from book import Book

class Depot(Base):
    __tablename__ = "depot"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    stock_quantity: Mapped[int] = mapped_column(nullable=True)
    distributor_id: Mapped[int] = mapped_column(ForeignKey("distributor.id"), nullable=False)
    distributor: Mapped[Distributor] = relationship("Distributor", back_populates="depots", uselist=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    book: Mapped[Book] = relationship("Book", back_populates="depots", uselist=False)

    stock_movements: Mapped[DepotStockMovement] = relationship("DepotStockMovement", back_populates="depot")

    __table_args__ = (
        CheckConstraint("stock_quantity >= 0", name="ck_stock_quantity"),
    )

    def __repr__(self):
        return f"> Depot({self.id}) : stock_quantity = {self.stock_quantity}"