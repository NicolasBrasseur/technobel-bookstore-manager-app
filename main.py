from fastapi import FastAPI

from routers.publisher import router as publisher_router

app = FastAPI()

app.include_router(publisher_router)

