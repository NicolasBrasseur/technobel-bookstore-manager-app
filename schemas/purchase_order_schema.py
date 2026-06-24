from pydantic import BaseModel
from datetime import datetime


class PurchaseOrderAddBook(BaseModel):
    book_isbn: int
    bookstore_id: int
    quantity: int


class PurchaseOrderRemoveBook(BaseModel):
    book_isbn: int
    bookstore_id: int
    quantity: int


class PurchaseOrderResponse(BaseModel):
    id: int
    status: str
    total_price: float | None
    order_date: datetime
    bookstore_id: int
    distributor_id: int

    model_config = {"from_attributes": True}