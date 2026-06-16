from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

class Depot(Base):
    __tablename__ = "depot"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)

    def __repr__(self):
        return f"Depot({self.id}) :"