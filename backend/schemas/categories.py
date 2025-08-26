from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    """Schema para criação de categoria"""
    name: str = Field(..., min_length=1, max_length=100)

    class Config:
        orm_mode = True


class CategoryResponse(BaseModel):
    """Schema de resposta para categoria"""
    category_id: int
    name: str

    class Config:
        orm_mode = True