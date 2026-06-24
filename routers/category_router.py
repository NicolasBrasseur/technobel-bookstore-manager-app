from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from services.category_service import add_new_category
from schemas.category_schema import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, session: Session = Depends(get_db)):
    try: return add_new_category(session, category.name)
    except ValueError as e: raise HTTPException(status_code=409, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))