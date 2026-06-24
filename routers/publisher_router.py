from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from services.publisher_service import add_new_publisher
from schemas.publisher_schema import PublisherCreate, PublisherResponse


router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.post("/", response_model=PublisherResponse)
def create_publisher(publisher: PublisherCreate, session: Session = Depends(get_db)):
    try: return add_new_publisher(session, publisher.name)
    except ValueError as e: raise HTTPException(status_code=409, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))