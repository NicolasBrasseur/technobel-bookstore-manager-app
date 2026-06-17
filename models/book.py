from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    isbn: Mapped[int] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(nullable=False)
    publisher_id: Mapped[int] = mapped_column(nullable=False)


    def __repr__(self):
        return f"Book({self.id}) : isbn = {self.isbn}, title = {self.title}, price = {self.price}"