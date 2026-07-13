from datetime import date as DateType

from sqlalchemy import func
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


def get_transactions(
    db: Session,
    category_id: int | None = None,
    transaction_type: schemas.TransactionType | None = None,
    start_date: DateType | None = None,
    end_date: DateType | None = None,
):
    query = db.query(models.Transaction)

    if category_id is not None:
        query = query.filter(models.Transaction.category_id == category_id)

    if transaction_type is not None:
        query = query.filter(models.Transaction.type == transaction_type)

    if start_date is not None:
        query = query.filter(models.Transaction.date >= start_date)

    if end_date is not None:
        query = query.filter(models.Transaction.date <= end_date)

    return query.all()


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


def get_monthly_summary(db: Session):
    month_label = func.strftime("%Y-%m", models.Transaction.date)

    rows = (
        db.query(
            month_label.label("month"),
            models.Transaction.type,
            func.sum(models.Transaction.amount).label("total"),
        )
        .group_by(month_label, models.Transaction.type)
        .order_by(month_label)
        .all()
    )

    summary_by_month = {}

    for month, transaction_type, total in rows:
        if month not in summary_by_month:
            summary_by_month[month] = {
                "month": month,
                "income": 0,
                "expense": 0,
                "balance": 0,
            }

        summary_by_month[month][transaction_type] = total

    for summary in summary_by_month.values():
        summary["balance"] = summary["income"] - summary["expense"]

    return list(summary_by_month.values())


def get_category_summary(db: Session):
    rows = (
        db.query(
            models.Category.id.label("category_id"),
            models.Category.name.label("category_name"),
            models.Category.type,
            func.sum(models.Transaction.amount).label("total"),
        )
        .join(models.Transaction)
        .group_by(models.Category.id, models.Category.name, models.Category.type)
        .order_by(models.Category.name)
        .all()
    )

    return [
        {
            "category_id": category_id,
            "category_name": category_name,
            "type": transaction_type,
            "total": total,
        }
        for category_id, category_name, transaction_type, total in rows
    ]
