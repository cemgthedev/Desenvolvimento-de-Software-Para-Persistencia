from datetime import datetime as dt
from models import Product
from utils.db import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Rota para criar um novo produto
@router.post("/products")
async def create_product(product: Product):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            INSERT INTO products (seller_id, title, description, price, category, quantity)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """,
            (
                product.seller_id,
                product.title,
                product.description,
                product.price,
                product.category,
                product.quantity,
            ),
        )
        connection.commit()

        product_id = cursor.fetchone()["id"]
        return {"message": f"Product with id={product_id} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para obter um produto pelo ID
@router.get("/products/{id}")
async def get_product(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id={id} not found")

        return {"product": product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para atualizar um produto pelo ID
@router.put("/products/{id}")
async def update_product(id: str, product: Product):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            UPDATE products
            SET seller_id = %s, title = %s, description = %s, price = %s, category = %s, quantity = %s
            WHERE id = %s
            """,
            (
                product.seller_id,
                product.title,
                product.description,
                product.price,
                product.category,
                product.quantity,
                id,
            ),
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Product with id={id} not found")

        return {"message": f"Product with id={id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para deletar um produto pelo ID
@router.delete("/products/{id}")
async def delete_product(id: str):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Product with id={id} not found")

        return {"message": f"Product with id={id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()

# Rota para buscar produtos com filtros
@router.get("/products")
async def get_products(
    seller_id: str = Query(None, description="ID do vendedor"),
    title: str = Query(None, description="Nome do produto"),
    min_price: float = Query(None, description="Preço mínimo do produto"),
    max_price: float = Query(None, description="Preço máximo do produto"),
    category: str = Query(None, description="Categoria do produto"),
    min_quantity: int = Query(None, description="Quantidade mínima do produto"),
    max_quantity: int = Query(None, description="Quantidade máxima do produto"),
):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        base_query = "SELECT * FROM products WHERE 1=1"
        filters = []
        params = []

        if seller_id:
            filters.append("seller_id = %s")
            params.append(seller_id)
        if title:
            filters.append("name ILIKE %s")
            params.append(f"%{title}%")
        if min_price:
            filters.append("price >= %s")
            params.append(min_price)
        if max_price:
            filters.append("price <= %s")
            params.append(max_price)
        if category:
            filters.append("category = %s")
            params.append(category)
        if min_quantity:
            filters.append("quantity >= %s")
            params.append(min_quantity)
        if max_quantity:
            filters.append("quantity <= %s")
            params.append(max_quantity)

        if filters:
            base_query += " AND " + " AND ".join(filters)

        cursor.execute(base_query, tuple(params))
        products = cursor.fetchall()

        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()