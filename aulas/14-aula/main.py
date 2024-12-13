from fastapi import FastAPI
from crud import list_users, create_user
from db import get_connection, create_tables
from psycopg2.extras import RealDictCursor

app = FastAPI()

create_tables()

@app.post("/users")
def create_user(nome: str, email: str):
    user_id = create_user(nome, email)
    return {"user_id": user_id}