from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from author import Author
    from bookstore import Bookstore
    from client import Client
    from distributor import Distributor

class Country(Base):
    __tablename__ = "country"

    identifier: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    vat: Mapped[float] = mapped_column(nullable=False)

    authors: Mapped[Author] = relationship("Author", back_populates="country")
    bookstores: Mapped[Bookstore] = relationship("Bookstore", back_populates="country")
    clients: Mapped[Client] = relationship("Client", back_populates="country")
    distributors: Mapped[Distributor] = relationship("Distributor", back_populates="operating_country")

    def __repr__(self):
        return f"> Country({self.id}) : name = {self.name} | vat = {self.vat}"