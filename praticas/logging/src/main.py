from fastapi import FastAPI
from services.books import router as books_router
from utils.generate_xml import generate_xml

app = FastAPI()

# Inicializando arquivo XML
generate_xml();

# Rota de teste
@app.get("/")
def read_root():
    return {"message": "Seja bem vindo a Books API"}

# Incluindo rotas de livros
app.include_router(books_router);