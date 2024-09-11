import streamlit as st
import pandas as pd
import io
from db_connection import insert_data_to_db  # Asegúrate de tener esta función en un módulo común

st.title('Combina Archivos de Excel')

st.header('Carga tus archivos de Excel')

uploaded_file_pacientes = st.file_uploader("D:/UNIVERSIDAD/6 semestre/Bases de datos/pacientes.xlsx", type=["xlsx"])
uploaded_file_tratamientos = st.file_uploader("D:/UNIVERSIDAD/6 semestre/Bases de datos/tratamientos.xlsx", type=["xlsx"])

if uploaded_file_pacientes and uploaded_file_tratamientos:
    # Leer los archivos subidos
    df_pacientes = pd.read_excel(uploaded_file_pacientes)
    df_tratamientos = pd.read_excel(uploaded_file_tratamientos)
    
    df_combinado = pd.merge(df_pacientes, df_tratamientos, on='ID_Paciente')

    st.write("Datos Combinados")
    st.dataframe(df_combinado)

    if st.button('Guardar en la base de datos'):
        try:
            insert_data_to_db(df_combinado, 'PACIENTES')  # Cambia 'nombre_de_tu_tabla' por el nombre real de tu tabla
            st.success('Datos guardados exitosamente en la base de datos.')
        except Exception as e:
            st.error(f"Error al guardar los datos: {e}")

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
