from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    """Model representing a product in the database."""
    product_id: str = Field(index=True, unique=True, primary_key=True)
    name: str
    description: str
    price: str
    category: str
    brand: str
    material: str
    color: str
    size: str
    created_at: datetime = Field(default_factory=datetime.now)
    
