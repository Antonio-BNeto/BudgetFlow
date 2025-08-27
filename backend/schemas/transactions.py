from pydantic import BaseModel, Field, field_validator
from datetime import date
from db.models import TransactionType

class TransactionCreate(BaseModel):
    """Schema for transaction creation"""
    type: str = Field(..., description="Transaction type: 'income' or 'expense'")
    amount: float = Field(..., gt=0, description="Transaction amount")
    date: str = Field(..., description="Transaction date in YYYY-MM-DD format")
    description: str = Field(..., description="Transaction description")
    category_id: int = Field(None, description="Associated category")

    @field_validator("type")
    def validate_type(cls, value):
        if value not in ["income", "expense"]:
            raise ValueError(f"Invalid transaction type. Allowed values are: 'income' or 'expense'")
        return TransactionType(value)

    @field_validator("date")
    def validate_date(cls, value):
        try:
            year, month, day = map(int, value.split("-"))
            return date(year, month, day)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    transaction_id: int
    type: str
    amount: float
    date: str
    description: str
    category_id: int
    
    @field_validator("type", mode="before")
    def convert_enum_to_string(cls, value):
        """Converte Enum para string"""
        if isinstance(value, TransactionType):
            return value.value
        return value

    @field_validator("date", mode="before")
    def convert_date_to_string(cls, value):
        """Converte date para string"""
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        return value

    model_config = {
        "from_attributes": True
    }