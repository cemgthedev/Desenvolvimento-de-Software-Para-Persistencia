from pydantic import BaseModel
from typing import Optional

class ProductModel(BaseModel):
    id: Optional[str]
    name: str
    description: str
    price: float
    in_store: bool