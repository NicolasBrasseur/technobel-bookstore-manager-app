from fastapi import FastAPI

from api.publisher import router as publisher_router

app = FastAPI()

app.include_router(publisher_router)

