from pydantic import BaseModel, Field, field_validator
from datetime import date

class BudgetCreate(BaseModel):
    """Schema for budget creation"""
    month: str = Field(..., description="Date in YYYY-MM format")
    limit: float = Field(..., gt=0, description="Limit for the budget")
    category_id: int = Field(None, description="Associated category")

    @field_validator("month")
    def validate_month(cls, value):
        try:
            # converte string YYYY-MM para objeto date
            year, month = map(int, value.split("-"))
            if not (1 <= month <= 12):
                raise ValueError("Invalid month. Month must be between 01 and 12.")
            return value
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM.")

class BudgetResponse(BaseModel):
    """Schema for budget response"""
    budget_id: int
    month: str
    limit: float
    category_id: int
    
    @field_validator("month", mode="before")
    def validate_month(cls, value):
        if isinstance(value, date):
            return value.strftime("%Y-%m")
        return value

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            date: lambda v: v.strftime("%Y-%m") if v else None
        }
    }