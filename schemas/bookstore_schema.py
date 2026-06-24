from pydantic import BaseModel


class BookstoreCreate(BaseModel):
    name: str
    country_identifier: str


class BookstoreResponse(BaseModel):
    id: int
    name: str
    country_identifier: str

    model_config = {"from_attributes": True}