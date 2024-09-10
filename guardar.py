import streamlit as st
import pandas as pd
import io
import mysql.connector
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Acceder a las variables de entorno definidas en el archivo .env
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Función para conectar a la base de datos
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
        st.error(f"Error al conectar a MySQL: {e}")
        return None

# Función para insertar datos en la base de datos
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

# Título de la aplicación
st.title('Combina Archivos de Excel')

# Sección para cargar los archivos de Excel
st.header('Carga tus archivos de Excel')

# Cargar archivos
uploaded_file_pacientes = st.file_uploader("Sube el archivo de Pacientes", type=["xlsx"])
uploaded_file_tratamientos = st.file_uploader("Sube el archivo de Tratamientos", type=["xlsx"])

if uploaded_file_pacientes and uploaded_file_tratamientos:
    # Leer los archivos subidos
    df_pacientes = pd.read_excel(uploaded_file_pacientes)
    df_tratamientos = pd.read_excel(uploaded_file_tratamientos)
    
    # Combinar los DataFrames
    df_combinado = pd.merge(df_pacientes, df_tratamientos, on='ID_Paciente')

    # Mostrar el DataFrame combinado
    st.write("Datos Combinados")
    st.dataframe(df_combinado)

    # Botón para guardar en la base de datos
    if st.button('Guardar en la base de datos'):
        try:
            insert_data_to_db(df_combinado, 'nombre_de_tu_tabla')  # Cambia 'nombre_de_tu_tabla' por el nombre real de tu tabla
            st.success('Datos guardados exitosamente en la base de datos.')
        except Exception as e:
            st.error(f"Error al guardar los datos: {e}")

    # Descargar el archivo combinado
    combined_file = io.BytesIO()
    with pd.ExcelWriter(combined_file, engine='openpyxl') as writer:
        df_combinado.to_excel(writer, index=False, sheet_name='Datos_Combinados')
    combined_file.seek(0)
    
    st.download_button(
        label="Descargar Datos Combinados",
        data=combined_file,
        file_name='Datos_Combinados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.info("Por favor, sube ambos archivos de Excel.")
