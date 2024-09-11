import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

print(f"Usuario: {db_user}")
print(f"Contraseña: {db_password}")
print(f"Host: {db_host}")
print(f"Base de datos: {db_name}")

if not all([db_user, db_password, db_host, db_name]):
    print("Error: Algunas variables de entorno no se han cargado correctamente.")
else:
 
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

      
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Conectado a MySQL Server versión {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"Conectado a la base de datos: {record}")

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("La conexión a MySQL se ha cerrado.")
