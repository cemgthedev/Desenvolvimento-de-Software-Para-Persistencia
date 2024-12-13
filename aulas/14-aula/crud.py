from db import get_connection

def create_user(nome: str, email: str):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO usuario (nome, email) VALUES (%s, %s) RETURNING id", (nome, email))
        connection.commit()
        print("User created successfully")
        
        user_id = cursor.fetchone()[0]
        return user_id
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()
            
def list_users():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuario")
        users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Error listing users: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()
        if 'cursor' in locals():
            cursor.close()