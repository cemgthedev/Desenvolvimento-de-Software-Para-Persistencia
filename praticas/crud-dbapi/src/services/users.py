from models import User
from utils.db import get_connection
from psycopg2.extras import RealDictCursor

from fastapi import APIRouter, HTTPException, Query

# Criar roteador
router = APIRouter()

# Rota para criar um novo usuário
@router.post("/users")
async def create_user(user: User):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("INSERT INTO users (name, age, cpf, gender, phone_number, address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (user.name, user.age, user.cpf, user.gender, user.phone_number, user.address, user.email, user.password))
        connection.commit()
        
        user_id = cursor.fetchone()["id"]
        return {"message": f"User with id={user_id} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()
    
@router.get("/users/{id}")
async def get_user(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
        connection.commit()
        
        user = cursor.fetchone()
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

@router.put("/users/{id}")
async def update_user(id: str, user: User):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            UPDATE users
            SET name = %s, age = %s, cpf = %s, gender = %s, phone_number = %s,
                address = %s, email = %s, password = %s
            WHERE id = %s""", (
                user.name,
                user.age,
                user.cpf,
                user.gender,
                user.phone_number,
                user.address,
                user.email,
                user.password,
                id,
            ),
        )
        connection.commit()
        return {"message": f"User with id {id} updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()
    
@router.delete("/users/{id}")
async def delete_user(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM users WHERE id = %s", (id, ))
        connection.commit()
        
        return {"message": f"User with id {id} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()
    
@router.get("/users")
async def get_users(
    name: str = Query(None, description="Nome do usuário"),
    address: str = Query(None, description="Endereço do usuário"),
    gender: str = Query(None, description="Gênero do usuário"),
    min_age: int = Query(None, description="Idade mínima do usuário"),
    max_age: int = Query(None, description="Idade.máxima do usuário"),
    email: str = Query(None, description="Email do usuário"),
    password: str = Query(None, description="Senha do usuário"),
):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        base_query = "SELECT * FROM users WHERE 1=1"
        filters = []
        params = []

        if name:
            filters.append("name ILIKE %s")
            params.append(f"%{name}%")
        if address:
            filters.append("address ILIKE %s")
            params.append(f"%{address}%")
        if gender:
            filters.append("gender = %s")
            params.append(gender)
        if min_age:
            filters.append("age >= %s")
            params.append(min_age)
        if max_age:
            filters.append("age <= %s")
            params.append(max_age)
        if email:
            filters.append("email = %s")
            params.append(email)
        if password:
            filters.append("password = %s")
            params.append(password)

        if filters:
            base_query += " AND " + " AND ".join(filters)

        cursor.execute(base_query, tuple(params))
        users = cursor.fetchall()
        
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()