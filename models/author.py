from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.country import Country

class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    country_identifier: Mapped[str] = mapped_column(ForeignKey("country.identifier"), nullable=True)
    country: Mapped[Country] = relationship("Country", back_populates="author", uselist=False)

    def __repr__(self):
        return f"Author({self.id}) : name = {self.name}, country_identifier = {self.country_identifier}"