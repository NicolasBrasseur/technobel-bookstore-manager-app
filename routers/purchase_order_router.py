from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.purchase_order_schema import PurchaseOrderAddBook, PurchaseOrderRemoveBook, PurchaseOrderResponse

from services.purchase_order_service import add_book_to_purchase_order, remove_book_from_purchase_order, display_all_purchases_of_bookstore, display_all_purchases_of_distributor, validate_all_purchase_orders, cancel_all_purchase_orders, packaged_purchase_order_of_bookstore, ship_purchase_order, deliver_purchase_order, buy_book, add_stock


router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])


@router.get("/bookstore/{bookstore_id}", response_model=list[PurchaseOrderResponse])
def get_bookstore_purchases(bookstore_id: int, session: Session = Depends(get_db)):
    try: return display_all_purchases_of_bookstore(session, bookstore_id)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.get("/distributor/{distributor_id}", response_model=list[PurchaseOrderResponse])
def get_distributor_purchases(distributor_id: int, session: Session = Depends(get_db)):
    try: return display_all_purchases_of_distributor(session, distributor_id)
    except ValueError as e: raise HTTPException(status_code=404, detail=str(e))


@router.post("/add-book")
def add_book(data: PurchaseOrderAddBook, session: Session = Depends(get_db)):
    try: return add_book_to_purchase_order(session, data.book_isbn, data.bookstore_id, data.quantity)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))


@router.post("/remove-book")
def remove_book(data: PurchaseOrderRemoveBook, session: Session = Depends(get_db)):
    try: return remove_book_from_purchase_order(session, data.book_isbn, data.bookstore_id, data.quantity)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate/{bookstore_id}")
def validate(bookstore_id: int, session: Session = Depends(get_db)):
    try: return validate_all_purchase_orders(session, bookstore_id)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel/{bookstore_id}")
def cancel(bookstore_id: int, session: Session = Depends(get_db)):
    try: return cancel_all_purchase_orders(session, bookstore_id)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/package/{distributor_id}/{bookstore_name}")
def package(distributor_id: int, bookstore_name: str, session: Session = Depends(get_db)):
    try: return packaged_purchase_order_of_bookstore(session, distributor_id, bookstore_name)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/ship/{distributor_id}/{bookstore_name}")
def ship(distributor_id: int, bookstore_name: str, session: Session = Depends(get_db)):
    try: return ship_purchase_order(session, distributor_id, bookstore_name)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/deliver/{distributor_id}/{bookstore_name}")
def deliver(distributor_id: int, bookstore_name: str, session: Session = Depends(get_db)):
    try: return deliver_purchase_order(session, distributor_id, bookstore_name)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/buy")
def buy(data: dict, session: Session = Depends(get_db)):
    try: return buy_book(session, data["bookstore_id"], data["book_isbn"], data["quantity"])
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))


@router.post("/stock")
def stock(data: dict, session: Session = Depends(get_db)):
    try: return add_stock(session, data["distributor_id"], data["book_isbn"], data["quantity"])
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))