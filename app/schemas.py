from datetime import date as DateType
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: TransactionType


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TransactionBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    date: DateType
    type: TransactionType
    category_id: int = Field(..., gt=0)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=1, max_length=255)
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )
    date: DateType | None = None
    type: TransactionType | None = None
    category_id: int | None = Field(default=None, gt=0)


class TransactionResponse(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
