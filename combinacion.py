import pandas as pd

df_pacientes = pd.read_excel('D:/UNIVERSIDAD/6 semestre/Bases de datos/Pacientes.xlsx')
df_tratamientos = pd.read_excel('D:/UNIVERSIDAD/6 semestre/Bases de datos/Tratamientos.xlsx')

df_combinado = pd.merge(df_pacientes, df_tratamientos, on='ID_Paciente')

df_combinado.to_excel('Datos_Combinados.xlsx', index=False)

print(df_combinado.head())
