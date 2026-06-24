from pydantic import BaseModel


class CountryCreate(BaseModel):
    identifier: str
    name: str
    vat: float


class CountryResponse(BaseModel):
    id: int
    identifier: str
    name: str
    vat: float

    model_config = {"from_attributes": True}