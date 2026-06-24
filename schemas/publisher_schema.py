from pydantic import BaseModel


class PublisherCreate(BaseModel):
    name: str


class PublisherResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}