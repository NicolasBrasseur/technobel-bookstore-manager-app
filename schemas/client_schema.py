from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    email: str
    country_identifier: str


class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    country_identifier: str

    model_config = {"from_attributes": True}