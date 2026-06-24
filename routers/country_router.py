from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from services.country_service import add_new_country
from schemas.country_schema import CountryCreate, CountryResponse


router = APIRouter(prefix="/countries", tags=["Countries"])


@router.post("/", response_model=CountryResponse)
def create_country(country: CountryCreate, session: Session = Depends(get_db)):
    try: return add_new_country(session, country.identifier, country.name, country.vat)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))