from certifi import where
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from config import db

app = FastAPI()

class Categoria(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    
class Item(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    categoria_id: Optional[str] = None
    
@app.get("/")
async def root():
    return {"message": f'Database: {db._database}'}
    
@app.post("/categorias")
async def create_categoria(categoria: Categoria):
    doc_ref = db.collection("categorias").document()
    doc_ref.set(categoria.model_dump())
    
    return {"id": doc_ref.id, "message": "Categoria criada com sucesso!"}

@app.get("/categorias")
async def get_categorias():
    categorias = []
    for doc in db.collection("categorias").stream():
        categorias.append(doc.to_dict())
        
    if(categorias):
       return {"message": "Categorias encontradas", "data": categorias}
    else:
        return {"message": "Nenhuma categoria encontrada"}

@app.post("/items")
async def create_item(item: Item):
    if item.categoria_id:
        cat_ref = db.collection("categorias").where("id", "==", item.categoria_id)
        if not cat_ref.get():
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
    doc_ref = db.collection("items").document()
    doc_ref.set(item.model_dump())
    return {"id": doc_ref.id, "message": "Item criado com sucesso!"}

@app.get("/items")
async def get_items():
    items = []
    for doc in db.collection("items").stream():
        items.append(doc.to_dict())
        
    if(items):
       return {"message": "Itens encontrados", "data": items}
    else:
        return {"message": "Nenhum item encontrado"}
    
@app.get("/items_da_categoria/{name}")
async def get_categoria(name: str):
    cat_ref = db.collection("categorias").where("name", "==", name)
    if not cat_ref.get():
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categorias = cat_ref.get()
    categoria_id = categorias[0].id
    cat_items = db.collection("items").where("categoria_id", "==", categoria_id).stream()
    items = []
    for doc in cat_items:
        items.append(doc.to_dict())
        
    if(items):
       return {"message": "Itens encontrados", "data": items}
    else:
        return {"message": "Nenhum item encontrado"}
    