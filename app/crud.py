from sqlalchemy.orm import Session

from app import models, schemas


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def get_categories(db: Session):
    return db.query(models.Category).all()
