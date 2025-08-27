from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    """Schema for category creation"""
    name: str = Field(..., min_length=1, max_length=100)

class CategoryResponse(BaseModel):
    """Schema for category response"""
    category_id: int
    name: str

    model_config = {
        "from_attributes": True
    }