from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

class BookstoreShelf(Base):
    __tablename__ = "bookstore_shelf"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)

    def __repr__(self):
        return f"Bookstore shelf({self.id}) :"