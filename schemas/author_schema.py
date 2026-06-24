from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    country_identifier: str


class AuthorResponse(BaseModel):
    id: int
    name: str
    country_identifier: str

    model_config = {
        "from_attributes": True
    }