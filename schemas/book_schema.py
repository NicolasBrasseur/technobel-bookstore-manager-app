from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class BookCreate(BaseModel):
    isbn: int
    title: str
    price: float
    publication_date: datetime
    category_name: str
    author_name: str
    author_country_identifier: str
    publisher_id: int


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class AuthorResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class PublisherResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class BookResponse(BaseModel):
    isbn: int
    title: str
    price: float
    publication_date: datetime

    category: CategoryResponse
    author: AuthorResponse
    publisher: PublisherResponse

    model_config = {"from_attributes": True}


class BookWithStockResponse(BaseModel):
    book: BookResponse
    quantity: int


class BookSalesResponse(BaseModel):
    book: BookResponse
    sales: int


class BookPriceInCountryResponse(BaseModel):
    country: str
    vat: float
    price: float