from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import categories


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Expenses API")

app.include_router(categories.router)
