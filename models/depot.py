from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Depot(Base):
    __tablename__ = "depot"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    stock_quantity: Mapped[int] = mapped_column(nullable=True)
    distributor_id: Mapped[int] = mapped_column(ForeignKey("distributor.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)

    def __repr__(self):
        return f"Depot({self.id}) : stock_quantity = {self.stock_quantity}"