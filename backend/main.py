from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from agents.product_cleaner import AgentCleaner
from pydantic import BaseModel
from typing import List, Optional
from db.database import create_db_and_tables, get_session
from models.product_model import Product
from sqlmodel import select

@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Startup event to create database and tables.
    """
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
agent = AgentCleaner()

class ProductInput(BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    category: Optional[str] = ""
    brand: Optional[str] = ""
    material: Optional[str] = ""
    color: Optional[str] = ""
    size: Optional[str] = ""

class ProductOutput(BaseModel):
    clean_product: dict


# Clean all the uploaded messy product data
@app.post("/clean-product", response_model=ProductOutput)
async def clean_product(product: ProductInput):
    """
    Endpoint to clean product data.
    Expects raw product data as a JSON object.
    """
    
    try:
        initial_state = {
            "raw_product": product.model_dump(),
            "cleaned_product": {},
            
        }

        result = agent.invoke(initial_state)

        return ProductOutput(clean_product=result["cleaned_product"])
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Save all the cleaned product data to the database
@app.post("/save-product")
async def save_product(product: ProductInput):
    """
    Endpoint to save cleaned product data to the database.
    Expects cleaned product data as a JSON object.
    """
    
    try:
        db_product = Product(**product.model_dump())
        
        with get_session() as session:
            session.add(db_product)
            session.commit()
            session.refresh(db_product)
        
        return {"message": "Product saved successfully", "product_id": db_product.product_id}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# Get all products endpoint
@app.get("/products", response_model=List[Product])
async def get_products():
    """
    Endpoint to retrieve all products from the database.
    Returns a list of products.
    """
    
    try:
        with get_session() as session:
            products = session.exec(select(Product)).all()
        
        return products
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Get a specific product by ID
@app.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Endpoint to retrieve a specific product by its ID.
    Returns the product data if found.
    """
    
    try:
        with get_session() as session:
            product = session.get(Product, product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Update product by ID
@app.put("/product/{product_id}")
async def update_product(product_id: str, product: ProductInput):
    """
    Endpoint to update a product by its ID.
    Expects updated product data as a JSON object.
    """
    
    try:
        with get_session() as session:
            existing_product = session.get(Product, product_id)
            if not existing_product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            for key, value in product.model_dump().items():
                setattr(existing_product, key, value)
            
            session.add(existing_product)
            session.commit()
            session.refresh(existing_product)
        
        return {"message": "Product updated successfully", "product_id": existing_product.product_id}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Delete product by ID
@app.delete("/product/{product_id}")
async def delete_product(product_id: str):
    """
    Endpoint to delete a product by its ID.
    Returns a success message if the product is deleted.
    """
    
    try:
        with get_session() as session:
            product = session.get(Product, product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            session.delete(product)
            session.commit()
        
        return {"message": "Product deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))