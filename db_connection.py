import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        raise Exception(f"Error al conectar a MySQL: {e}")

def insert_data_to_db(df, table_name):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        for index, row in df.iterrows():
            columns = ', '.join(df.columns)
            values = ', '.join(['%s'] * len(row))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(sql, tuple(row))
        connection.commit()
        cursor.close()
        connection.close()

def create_table():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS pacientes (
            ID_Tratamiento INT,
            ID_Paciente INT,
            Medicación VARCHAR(255),
            Terapia VARCHAR(255),
            Fecha_Inicio DATE,
            Nombre VARCHAR(255),
            Edad INT,
            Diagnóstico VARCHAR(255),
            Fecha_Ingreso DATE,
            PRIMARY KEY (ID_Tratamiento, ID_Paciente)  -- Ajusta la clave primaria según tus necesidades
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()


create_table()
