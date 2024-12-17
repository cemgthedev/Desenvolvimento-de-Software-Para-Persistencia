from models import *
from utils.db import execute_script
from services.users import router as users_router
from services.messages import router as messages_router
from services.products import router as products_router
from services.favorites import router as favorites_router
from services.sales import router as sales_router
from services.analysis import router as analysis_router

from fastapi import FastAPI

app = FastAPI()

# Criando as tabelas
execute_script("./scripts/create-tables.sql")

# Rota de teste
@app.get("/")
def read_root():
    return {"message": "Seja bem vindo a Lojita"}

# Rota para popular as tabelas
@app.get("/populate")
def populate():
    try:
        execute_script("./scripts/populate-tables.sql")
        return {"message": "Tabelas populadas com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

# Incluindo rotas de usuários
app.include_router(users_router);

# Incluindo rotas de mensagens
app.include_router(messages_router);

# Incluindo rotas de produtos
app.include_router(products_router);

# Incluindo rotas de favoritos
app.include_router(favorites_router);

# Incluindo rotas de vendas
app.include_router(sales_router);

# Incluindo rotas de análise
app.include_router(analysis_router);