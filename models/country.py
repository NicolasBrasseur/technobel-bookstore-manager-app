from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.author import Author

class Country(Base):
    __tablename__ = "country"

    identifier: Mapped[str] = mapped_column(String(2), Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    vat: Mapped[float] = mapped_column(nullable=False)

    authors: Mapped[Author] = relationship("Author", back_populates="country")

    def __repr__(self):
        return f"Country({self.id}) : name = {self.name}, vat = {self.vat}"