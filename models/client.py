from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    country_identifier: Mapped[str] = mapped_column(String(2), nullable=False)

    def __repr__(self):
        return f"Client({self.id}) : name = {self.name}, country_identifier = {self.country_identifier}"