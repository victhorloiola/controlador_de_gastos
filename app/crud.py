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


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.model_dump())

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


def get_transactions(db: Session):
    return db.query(models.Transaction).all()


def get_transaction(db: Session, transaction_id: int):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )


def update_transaction(
    db: Session,
    db_transaction: models.Transaction,
    transaction_update: schemas.TransactionUpdate,
):
    update_data = transaction_update.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in update_data.items():
        setattr(db_transaction, field, value)

    db.commit()
    db.refresh(db_transaction)

    return db_transaction


def delete_transaction(db: Session, db_transaction: models.Transaction):
    db.delete(db_transaction)
    db.commit()
