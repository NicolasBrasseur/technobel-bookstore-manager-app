from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from services.distributor_service import add_new_distributor
from schemas.distributor_schema import DistributorCreate, DistributorResponse


router = APIRouter(prefix="/distributors", tags=["Distributors"])


@router.post("/", response_model=DistributorResponse)
def create_distributor(distributor: DistributorCreate, session: Session = Depends(get_db)):
    try: return add_new_distributor(session, distributor.name, distributor.operating_country_identifier)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))