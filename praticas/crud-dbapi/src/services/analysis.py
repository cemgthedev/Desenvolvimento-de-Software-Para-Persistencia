from models import *
from utils.db import get_connection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Rota para criar uma nova venda
@router.get("/expenses")
def get_expenses(
    user_id: str = Query(None, description="Id do usuário"),
    min_expense: float = Query(None, description="Gasto total mínimo"),
    max_expense: float = Query(None, description="Gasto total máximo"),
    min_qtd_compras: int = Query(None, description="Quantidade mínima de compras"),
    max_qtd_compras: int = Query(None, description="Quantidade máxima de compras"),
    min_qtd_favoritos: int = Query(None, description="Quantidade mínima de favoritos"),
    max_qtd_favoritos: int = Query(None, description="Quantidade máxima de favoritos"),
):
    try:
        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Base query
        base_query = """
            SELECT 
                u.id AS usuario_id,
                u.name AS usuario_nome,
                COALESCE(SUM(s.quantity * p.price), 0) AS gasto_total,
                COALESCE(AVG(s.quantity * p.price), 0) AS media_gasto,
                COALESCE(COUNT(s.id), 0) AS qtd_compras,
                COALESCE(COUNT(f.id), 0) AS qtd_favoritos
            FROM 
                users u
            LEFT JOIN 
                sales s ON s.buyer_id = u.id
            LEFT JOIN 
                products p ON s.product_id = p.id
            LEFT JOIN 
                favorites f ON f.user_id = u.id
            WHERE 
                1=1
        """

        filters = []
        having_filters = []
        params = []

        # Filtro no WHERE
        if user_id:
            filters.append("u.id = %s")
            params.append(user_id)

        # Filtros com agregação no HAVING
        if min_expense is not None:
            having_filters.append("COALESCE(SUM(s.quantity * p.price), 0) >= %s")
            params.append(min_expense)
        if max_expense is not None:
            having_filters.append("COALESCE(SUM(s.quantity * p.price), 0) <= %s")
            params.append(max_expense)
        if min_qtd_compras is not None:
            having_filters.append("COALESCE(COUNT(s.id), 0) >= %s")
            params.append(min_qtd_compras)
        if max_qtd_compras is not None:
            having_filters.append("COALESCE(COUNT(s.id), 0) <= %s")
            params.append(max_qtd_compras)
        if min_qtd_favoritos is not None:
            having_filters.append("COALESCE(COUNT(f.id), 0) >= %s")
            params.append(min_qtd_favoritos)
        if max_qtd_favoritos is not None:
            having_filters.append("COALESCE(COUNT(f.id), 0) <= %s")
            params.append(max_qtd_favoritos)

        # Aplica filtros WHERE
        if filters:
            base_query += " AND " + " AND ".join(filters)

        # Adiciona o GROUP BY
        base_query += """
            GROUP BY 
                u.id, u.name
        """

        # Aplica filtros HAVING
        if having_filters:
            base_query += " HAVING " + " AND ".join(having_filters)

        # Finaliza com ORDER BY
        base_query += " ORDER BY gasto_total DESC"

        # Executa a query
        cursor.execute(base_query, tuple(params))
        expenses = cursor.fetchall()
        return {"expenses": expenses}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()