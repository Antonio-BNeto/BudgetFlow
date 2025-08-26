from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date

class BudgetCreate(BaseModel):
    """Schema para criação de budget"""
    month: str = Field(..., regex=r"^(0[1-9]|1[0-2])-(\d{4})$", description="Mês no formato MM-AAAA")
    limit: Decimal = Field(..., gt=0, description="Valor do orçamento")
    category_id: int = Field(None, description="Categoria associada")

    class Config:
        orm_mode = True 


class BudgetResponse(BaseModel):
    """Schema de resposta para budget"""
    budget_id: int
    limit: Decimal
    category_id: int

    class Config:
        orm_mode = True