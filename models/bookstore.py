from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Bookstore(Base):
    __tablename__ = "bookstore"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    country_identifier: Mapped[str] = mapped_column(ForeignKey("country.identifier"), nullable=False)

    def __repr__(self):
        return f"Bookstore({self.id}) : name = {self.name}, country_identifier = {self.country_identifier}"