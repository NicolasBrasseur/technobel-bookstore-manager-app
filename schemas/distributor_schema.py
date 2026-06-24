from pydantic import BaseModel


class DistributorCreate(BaseModel):
    name: str
    operating_country_identifier: str


class DistributorResponse(BaseModel):
    id: int
    name: str
    operating_country_identifier: str

    model_config = {"from_attributes": True}