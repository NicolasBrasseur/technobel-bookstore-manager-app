from fastapi import FastAPI

from routers.author_router import router as author_router
from routers.book_router import router as book_router
from routers.bookstore_router import router as bookstore_router
from routers.category_router import router as category_router
from routers.client_router import router as client_router
from routers.country_router import router as country_router
from routers.distributor_router import router as distributor_router
from routers.publisher_router import router as publisher_router
from routers.purchase_order_router import router as purchase_order_router


app = FastAPI(
    title="Bookstore API",
    description="API de gestion de librairie avec commandes, stock et distribution",
    version="1.0.0"
)


# -----------------------
# ROUTERS REGISTRATION
# -----------------------

app.include_router(author_router)
app.include_router(book_router)
app.include_router(bookstore_router)
app.include_router(category_router)
app.include_router(client_router)
app.include_router(country_router)
app.include_router(distributor_router)
app.include_router(publisher_router)
app.include_router(purchase_order_router)