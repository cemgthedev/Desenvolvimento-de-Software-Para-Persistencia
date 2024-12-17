from models import Favorite
from utils.db import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Rota para criar um novo favorito
@router.post("/favorites")
async def create_favorite(favorite: Favorite):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            INSERT INTO favorites (user_id, product_id)
            VALUES (%s, %s) RETURNING id
            """,
            (favorite.user_id, favorite.product_id),
        )
        connection.commit()

        favorite_id = cursor.fetchone()["id"]
        return {"message": f"Favorite with id={favorite_id} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para obter um favorito pelo ID
@router.get("/favorites/{id}")
async def get_favorite(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM favorites WHERE id = %s", (id,))
        favorite = cursor.fetchone()

        if not favorite:
            raise HTTPException(status_code=404, detail=f"Favorite with id={id} not found")

        return {"favorite": favorite}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para deletar um favorito pelo ID
@router.delete("/favorites/{id}")
async def delete_favorite(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM favorites WHERE id = %s", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Favorite with id={id} not found")

        return {"message": f"Favorite with id={id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para buscar favoritos com filtros
@router.get("/favorites")
async def get_favorites(
    user_id: str = Query(None, description="ID do usuário"),
):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        base_query = "SELECT * FROM favorites WHERE 1=1"
        filters = []
        params = []

        if user_id:
            filters.append("user_id = %s")
            params.append(user_id)

        if filters:
            base_query += " AND " + " AND ".join(filters)

        cursor.execute(base_query, tuple(params))
        favorites = cursor.fetchall()

        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()