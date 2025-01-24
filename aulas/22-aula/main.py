from fastapi import FastAPI, HTTPException
from database import db
from bson import ObjectId
import logging
import pymongo
from schemas import Product, ProductCreate

logging.basicConfig()
logger = logging.getLogger("pymongo").setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Seja bem vindo!!"}

@app.post("/products", response_model=dict)
def create_product(data: ProductCreate):
    try:
        result = db.items.insert_one(data)
        return {"message": f"Item criado com sucesso!, id: {str(result.inserted_id)}"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/products", list[Product])
def get_products():
    try:
        items = list(db.items.find())
        for item in items:
            item["_id"] = str(item["_id"])
        return items
    except Exception as e:
        return {"error": str(e)}
    
@app.delete("/products/{id}", response_model=dict)
def delete_product(id: str):
    try:
        result = db.items.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Item deletado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/products/{id}", Product)
def get_product(id: str):
    try:
        item = db.items.find_one({"_id": ObjectId(id)})
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        item["_id"] = str(item["_id"])
        return item
    except Exception as e:
        return {"error": str(e)}
    
@app.put("/products/{id}", response_model=Product)
def update_product(id: str, data: ProductCreate):
    try:
        result = db.items.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Item atualizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}