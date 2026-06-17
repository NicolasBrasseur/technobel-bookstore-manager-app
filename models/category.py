from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from book import Book

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    books: Mapped[Book] = relationship("Book", back_populates="category")

    def __repr__(self):
        return f"Category({self.id}) : name = {self.name}"