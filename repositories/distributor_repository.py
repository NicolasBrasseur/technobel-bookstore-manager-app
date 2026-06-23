from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.distributor import Distributor
from models.depot import Depot
from models.book import Book

def create_distributor(session: Session, name:str, operating_country_identifier:str):
    distributor = Distributor(name=name, operating_country_identifier=operating_country_identifier)
    session.add(distributor)
    return distributor

def get_distributor_by_name_and_country(session:Session, name:str, operating_country_identifier:str):
    stmt = select(Distributor).where(and_(Distributor.name == name, Distributor.operating_country_identifier == operating_country_identifier))
    distributor = session.execute(stmt).scalar_one_or_none()
    return distributor

def get_distributor_with_book_stock(session:Session, book_isbn:int):
    stmt = (select(Distributor, Depot.stock_quantity).distinct()
            .join(Distributor.depots)
            .join(Depot.book)
            .where(Book.isbn == book_isbn)
            .order_by(Depot.stock_quantity.desc())
    )
    distributor = session.execute(stmt).unique().first()
    return distributor