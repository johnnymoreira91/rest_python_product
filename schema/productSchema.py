from pydantic import BaseModel
from typing import Optional

class ProductSchemaInput(BaseModel):
    name: str
    description: str
    active: bool
    price: int
    quantity: int

class ProductSchemaOutput(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    price: int
    quantity: int

    class Config:
        orm_mode = True

class ProductSchemaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    price: Optional[int] = None
    quantity: Optional[int] = None