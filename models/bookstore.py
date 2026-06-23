from database.database import Base
from sqlalchemy import Identity, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bookstore_shelf import BookstoreShelf
    from country import Country
    from purchase_order import PurchaseOrder

class Bookstore(Base):
    __tablename__ = "bookstore"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    country_identifier: Mapped[str] = mapped_column(ForeignKey("country.identifier"), nullable=False)
    country: Mapped[Country] = relationship("Country", back_populates="bookstores", uselist=False)

    shelves: Mapped[BookstoreShelf] = relationship("BookstoreShelf", back_populates="bookstore")
    orders: Mapped[PurchaseOrder] = relationship("PurchaseOrder", back_populates="bookstore")

    __table_args__ = (
        UniqueConstraint(name, country_identifier, name="uk_bookstore"),
    )

    def __repr__(self):
        return f"> Bookstore({self.id}) : name = {self.name} | country_identifier = {self.country_identifier}"