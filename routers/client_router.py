from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from services.client_service import add_new_client
from schemas.client_schema import ClientCreate, ClientResponse


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, session: Session = Depends(get_db)):
    try: return add_new_client(session, client.name, client.email, client.country_identifier)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=500, detail=str(e))