from fastapi import Depends, APIRouter
from database.database import get_db
from sqlalchemy.orm import Session

from repositories.publisher_repository import create_publisher, display_all_publishers

router = APIRouter(
    prefix="/publisher",
    tags=["Publisher"]
)

@router.get("/")
def get_publishers(session: Session = Depends(get_db)):
    return display_all_publishers(session)