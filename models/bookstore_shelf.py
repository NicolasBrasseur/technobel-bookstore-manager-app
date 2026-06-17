from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bookstore import Bookstore
    from book import Book
    from shelf_stock_movement import ShelfStockMovement

class BookstoreShelf(Base):
    __tablename__ = "bookstore_shelf"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=True)
    bookstore_id: Mapped[int] = mapped_column(ForeignKey("bookstore.id"), nullable=False)
    bookstore: Mapped[Bookstore] = relationship("Bookstore", back_populates="shelves", uselist=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    book: Mapped[Book] = relationship("Book", back_populates="bookstore_shelves", uselist=False)

    stock_movements: Mapped[ShelfStockMovement] = relationship("ShelfStockMovement", back_populates="bookstore_shelf")

    def __repr__(self):
        return f"Bookstore shelf({self.id}) : quantity = {self.quantity}"