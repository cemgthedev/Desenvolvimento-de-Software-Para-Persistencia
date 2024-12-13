import psycopg2
from psycopg2 import OperationalError

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="123456",
            port="5432"
        )
        return connection
    except OperationalError:
        print("Error connecting to the database")
        return None
    
def create_tables():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        command = [
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS produto (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                preco FLOAT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pedido (
                id SERIAL PRIMARY KEY,
                data_pedido DATE NOT NULL,
                status VARCHAR(50) NOT NULL,
                usuario_id INT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuario(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pedido_produto (
                id SERIAL PRIMARY KEY,
                pedido_id INT NOT NULL,
                produto_id INT NOT NULL,
                quantidade INT NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedido(id),
                FOREIGN KEY (produto_id) REFERENCES produto(id)
            )
            """
        ]

        for command in command:
            cursor.execute(command)
        connection.commit()
        print("Tables created successfully!")
    except OperationalError:
        print("Error connecting to the database")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            connection.close()