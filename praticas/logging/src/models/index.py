from pydantic import BaseModel
from typing import Optional

# Classe Book
class Book(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    year: int
    genre: str