from pydantic import BaseModel
from typing import List

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    
class Pedido(BaseModel):
    id: int
    data_pedido: str
    status: str
    usuario_id: int
    
class Produto(BaseModel):
    id: int
    nome: str
    preco: float

class PedidoProduto(BaseModel):
    id: int
    pedido_id: int
    produto_id: int
    quantidade: int