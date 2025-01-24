from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    in_store: bool
    
class Product(ProductCreate):
    id: str