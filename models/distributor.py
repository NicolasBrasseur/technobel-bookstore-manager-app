from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from depot import Depot
    from country import Country
    from purchase_order import PurchaseOrder

class Distributor(Base):
    __tablename__ = "distributor"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    operating_country_identifier: Mapped[str] = mapped_column(ForeignKey("country.identifier"), nullable=False)
    operating_country: Mapped[Country] = relationship("Country", back_populates="distributors", uselist=False) 

    depots: Mapped[Depot] = relationship("Depot", back_populates="distributor")
    orders: Mapped[PurchaseOrder] = relationship("PurchaseOrder", back_populates="distributor")

    def __repr__(self):
        return f"Distributor({self.id}) : name = {self.name}, operating_country_identifier = {self.operating_country_identifier}"