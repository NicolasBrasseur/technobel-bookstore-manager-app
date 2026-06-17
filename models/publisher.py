from database.database import Base
from sqlalchemy import Identity, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Publisher(Base):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f"Publisher({self.id}) : name={self.name}"