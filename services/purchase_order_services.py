from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repositories.purchase_order_repository import create_purchase, get_all_purchases_of_bookstore, get_all_purchases_of_distributor

def display_all_purchases_of_bookstore(session:Session, bookstore_id:int):
    purchases = get_all_purchases_of_bookstore(session, bookstore_id)
    if not purchases:
        print("There are no purchases order")
        return None
    
    for purchase in purchases:
        print(purchase)

    return purchases

def display_all_purchases_of_distributor(session:Session, distributor_id:int):
    purchases = get_all_purchases_of_distributor(session, distributor_id)
    if not purchases:
        print("There are no purchases order")
        return None
    
    for purchase in purchases:
        print(purchase)

    return purchases