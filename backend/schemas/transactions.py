from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date

class TransactionCreate(BaseModel):
    """Schema para criação de transação"""
    description: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0, description="Valor da transação")
    date: date
    category_id: int = Field(None, description="Categoria associada")

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    """Schema de resposta para transação"""
    transaction_id: int
    description: str
    amount: Decimal
    date: date
    category_id: int

    class Config:
        orm_mode = True