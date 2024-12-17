from datetime import datetime as dt
from models import Sale
from utils.db import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Rota para criar uma nova venda
@router.post("/sales")
async def create_sale(sale: Sale):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            INSERT INTO sales (seller_id, buyer_id, product_id, quantity, created_at)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """,
            (sale.seller_id, sale.buyer_id, sale.product_id, sale.quantity, sale.created_at or dt.now()),
        )
        connection.commit()

        sale_id = cursor.fetchone()["id"]
        return {"message": f"Sale with id={sale_id} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para obter uma venda pelo ID
@router.get("/sales/{id}")
async def get_sale(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM sales WHERE id = %s", (id,))
        sale = cursor.fetchone()

        if not sale:
            raise HTTPException(status_code=404, detail=f"Sale with id={id} not found")

        return {"sale": sale}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para deletar uma venda pelo ID
@router.delete("/sales/{id}")
async def delete_sale(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM sales WHERE id = %s", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Sale with id={id} not found")

        return {"message": f"Sale with id={id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para buscar vendas com filtros
@router.get("/sales")
async def get_sales(
    seller_id: str = Query(None, description="ID do vendedor"),
    buyer_id: str = Query(None, description="ID do comprador"),
    min_quantity: int = Query(None, description="Quantidade mínima de produtos"),
    max_quantity: int = Query(None, description="Quantidade máxima de produtos"),
    min_datetime: dt = Query(None, description="Data e horário mínimo da compra"),
    max_datetime: dt = Query(None, description="Data e horário máximo da compra"),
):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        base_query = "SELECT * FROM sales WHERE 1=1"
        filters = []
        params = []

        if seller_id:
            filters.append("seller_id = %s")
            params.append(seller_id)
        if buyer_id:
            filters.append("buyer_id = %s")
            params.append(buyer_id)
        if min_quantity:
            filters.append("quantity >= %s")
            params.append(min_quantity)
        if max_quantity:
            filters.append("quantity <= %s")
            params.append(max_quantity)
        if min_datetime:
            filters.append("created_at >= %s")
            params.append(min_datetime)
        if max_datetime:
            filters.append("created_at <= %s")
            params.append(max_datetime)

        if filters:
            base_query += " AND " + " AND ".join(filters)

        cursor.execute(base_query, tuple(params))
        sales = cursor.fetchall()

        return {"sales": sales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()