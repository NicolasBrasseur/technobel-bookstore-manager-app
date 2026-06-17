from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Distributor(Base):
    __tablename__ = "distributor"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    operating_country_identifier: Mapped[str] = mapped_column(ForeignKey("country.identifier"), nullable=False)

    def __repr__(self):
        return f"Distributor({self.id}) : name = {self.name}, operating_country_identifier = {self.operating_country_identifier}"