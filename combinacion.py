import pandas as pd

# Cargar los archivos de Excel en DataFrames
df_pacientes = pd.read_excel('D:/UNIVERSIDAD/6 semestre/Bases de datos/Pacientes.xlsx')
df_tratamientos = pd.read_excel('D:/UNIVERSIDAD/6 semestre/Bases de datos/Tratamientos.xlsx')

# Combinar ambos DataFrames utilizando la columna 'ID_Paciente' como clave común
df_combinado = pd.merge(df_pacientes, df_tratamientos, on='ID_Paciente')

# Guardar el DataFrame combinado en un nuevo archivo Excel
df_combinado.to_excel('Datos_Combinados.xlsx', index=False)

# Opcional: Mostrar las primeras filas del DataFrame combinado
print(df_combinado.head())
