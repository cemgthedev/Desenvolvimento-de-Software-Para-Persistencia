from datetime import datetime as dt
from models import Message
from utils.db import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Rota para criar uma nova mensagem
@router.post("/messages")
async def create_message(message: Message):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            INSERT INTO messages (user_sent_id, user_received_id, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """,
            (message.user_sent_id, message.user_received_id, message.title, message.description, dt.now()),
        )
        connection.commit()

        message_id = cursor.fetchone()["id"]
        return {"message": f"Message with id={message_id} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para obter uma mensagem pelo ID
@router.get("/messages/{id}")
async def get_message(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM messages WHERE id = %s", (id,))
        message = cursor.fetchone()

        if not message:
            raise HTTPException(status_code=404, detail=f"Message with id={id} not found")

        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para atualizar uma mensagem pelo ID
@router.put("/messages/{id}")
async def update_message(id: str, message: Message):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            UPDATE messages
            SET user_sent_id = %s, user_received_id = %s, title = %s, description = %s
            WHERE id = %s
            """,
            (message.user_sent_id, message.user_received_id, message.title, message.description, id),
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Message with id={id} not found")

        return {"message": f"Message with id={id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para deletar uma mensagem pelo ID
@router.delete("/messages/{id}")
async def delete_message(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM messages WHERE id = %s", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Message with id={id} not found")

        return {"message": f"Message with id={id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para buscar mensagens com filtros
@router.get("/messages")
async def get_messages(
    subject: str = Query(None, description="Assunto da mensagem"),
    min_datetime: dt = Query(None, description="Data e horário mínimo da mensagem"),
    max_datetime: dt = Query(None, description="Data e horário máximo da mensagem"),
):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        base_query = "SELECT * FROM messages WHERE 1=1"
        filters = []
        params = []

        if subject:
            filters.append("title ILIKE %s")
            params.append(f"%{subject}%")
        if min_datetime:
            filters.append("created_at >= %s")
            params.append(min_datetime)
        if max_datetime:
            filters.append("created_at <= %s")
            params.append(max_datetime)

        if filters:
            base_query += " AND " + " AND ".join(filters)

        cursor.execute(base_query, tuple(params))
        messages = cursor.fetchall()

        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()