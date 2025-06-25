from pydantic import BaseModel
from typing import Optional, List

class RawProduct(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    brand: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None

class CleanedProduct(BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    category: str
    brand: str
    material: str
    color: str
    size: str