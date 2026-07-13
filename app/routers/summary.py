from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/monthly", response_model=list[schemas.MonthlySummaryResponse])
def get_monthly_summary(db: Session = Depends(get_db)):
    return crud.get_monthly_summary(db=db)


@router.get("/category", response_model=list[schemas.CategorySummaryResponse])
def get_category_summary(db: Session = Depends(get_db)):
    return crud.get_category_summary(db=db)
