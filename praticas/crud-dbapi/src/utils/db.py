import psycopg2
from psycopg2 import OperationalError

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="lista",
            user="postgres",
            password="12345678",
            port="5432"
        )
        return connection
    except OperationalError:
        print("Error connecting to the database")
        return None
    
def execute_script(sql_file_path: str):
    try:
        with open(sql_file_path, "r", encoding='utf-8') as file:
            sql_commands = file.read()
        
        connection = get_connection()
        cursor = connection.cursor()

        commands = sql_commands.strip().split(";")
        for command in commands:
            if command.strip():
                cursor.execute(command)
                connection.commit()
        print("Commands executed successfully")
    except OperationalError:
        print("Error connecting to the database")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            connection.close()