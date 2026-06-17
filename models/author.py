from database.database import Base
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    country_identifier: Mapped[str] = mapped_column(String(2), nullable=True) 
    # TODO: Finish author to country foreign key

    def __repr__(self):
        return f"Author({self.id}) : name = {self.name}, country_identifier = {self.country_identifier}"