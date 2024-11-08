from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": "Welcome to Fastapi!"}

class Item(BaseModel):
    name: str
    valor: float
    description: Union[bool, None] = None
    
items_db = {}

@app.post("/add_item")
def create_item(item: Item):
    items_db[item.name] = item
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int, nome: Union[str, None] = None):
    
    if item_id in items_db:
        return items_db[item_id]
    else:
        return {"Error": "Item not found"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id in items_db:
        items_db[item_id] = item
        return item
    else:
        return {"Error": "Item not found"}