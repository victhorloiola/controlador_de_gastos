from datetime import date as DateType

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/transactions", tags=["transactions"])


def validate_category_for_transaction(
    db: Session,
    category_id: int,
    transaction_type: schemas.TransactionType,
):
    category = crud.get_category(db=db, category_id=category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if category.type != transaction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category type must match transaction type",
        )


def get_transaction_or_404(db: Session, transaction_id: int):
    transaction = crud.get_transaction(db=db, transaction_id=transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    return transaction


@router.post(
    "",
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    validate_category_for_transaction(
        db=db,
        category_id=transaction.category_id,
        transaction_type=transaction.type,
    )

    return crud.create_transaction(db=db, transaction=transaction)


@router.get("", response_model=list[schemas.TransactionResponse])
def list_transactions(
    category_id: int | None = Query(default=None, gt=0),
    transaction_type: schemas.TransactionType | None = Query(
        default=None,
        alias="type",
    ),
    start_date: DateType | None = None,
    end_date: DateType | None = None,
    db: Session = Depends(get_db),
):
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )

    return crud.get_transactions(
        db=db,
        category_id=category_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    return get_transaction_or_404(db=db, transaction_id=transaction_id)


@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
):
    db_transaction = get_transaction_or_404(
        db=db,
        transaction_id=transaction_id,
    )

    next_category_id = transaction_update.category_id or db_transaction.category_id
    next_type = transaction_update.type or db_transaction.type

    validate_category_for_transaction(
        db=db,
        category_id=next_category_id,
        transaction_type=next_type,
    )

    return crud.update_transaction(
        db=db,
        db_transaction=db_transaction,
        transaction_update=transaction_update,
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    db_transaction = get_transaction_or_404(
        db=db,
        transaction_id=transaction_id,
    )

    crud.delete_transaction(db=db, db_transaction=db_transaction)
