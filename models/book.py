from database.database import Base
from sqlalchemy import Identity, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from category import Category
    from author import Author
    from publisher import Publisher
    from bookstore_shelf import BookstoreShelf
    from depot import Depot
    from order_book import OrderBook

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    isbn: Mapped[int] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(nullable=True)
    publication_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    category: Mapped[Category] = relationship("Category", back_populates="books", uselist=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    author: Mapped[Author] = relationship("Author", back_populates="books", uselist=False)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"), nullable=False)
    publisher: Mapped[Publisher] = relationship("Publisher", back_populates="books", uselist=False)

    bookstore_shelves: Mapped[BookstoreShelf] = relationship("BookstoreShelf", back_populates="book")
    depots: Mapped[Depot] = relationship("Depot", back_populates="book")
    order_books: Mapped[OrderBook] = relationship("OrderBook", back_populates="book")

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_price"),
    )


    def __repr__(self):
        return f"> Book({self.id}) : isbn = {self.isbn} | title = {self.title} | price = {self.price}"