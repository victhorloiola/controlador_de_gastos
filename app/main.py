from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import categories, summary, transactions


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Expenses API")


@app.get("/")
def read_root():
    return {
        "message": "API de Controle de Gastos Pessoais",
        "docs": "/docs",
    }


app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(summary.router)
