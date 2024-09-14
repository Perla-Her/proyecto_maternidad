import pandas as pd
import matplotlib.pyplot as plt


mortalidad_materna = pd.read_csv('mortalidad_materna.csv')

columnas_bd = ['ENTIDAD_RESIDENCIAD', 'EDAD_QUINQUENALD', 'CAUSA_CIE_4D', 'DERECHOHABIENCIAD', 'ANIO_DEFUNCION']

mortalidad = mortalidad_materna[columnas_bd]

mortalidad_filtrada = mortalidad[mortalidad['CAUSA_CIE_4D'].str.contains('aborto', case=False, na=False)]

agrupacion_anual = mortalidad_filtrada.groupby(['ANIO_DEFUNCION', 'CAUSA_CIE_4D']).agg({
    'ENTIDAD_RESIDENCIAD': 'count',
}).rename(columns={'ENTIDAD_RESIDENCIAD': 'CONTEO_POR_ESTADO'})

agrupacion_anual = agrupacion_anual.sort_values(by=('CONTEO_POR_ESTADO'), ascending=False).reset_index()

df_resultado = pd.merge(mortalidad_filtrada, agrupacion_anual, on=['ANIO_DEFUNCION', 'CAUSA_CIE_4D'], how='left')


# print(df_resultado)

conteo_por_año = df_resultado.groupby('ANIO_DEFUNCION').size()

df_resultado.groupby('ANIO_DEFUNCION')['CONTEO_POR_ESTADO'].sum().plot(kind='bar')
plt.xlabel('Año')
plt.ylabel('Número de casos')
plt.title('Número de casos de aborto por año')
plt.show()


conteo_por_estado = df_resultado.groupby('ENTIDAD_RESIDENCIAD').size()

df_resultado.groupby('ENTIDAD_RESIDENCIAD')['CONTEO_POR_ESTADO'].sum().plot(kind='bar')
plt.xlabel('Año')
plt.ylabel('Número de casos')
plt.title('Número de casos de aborto por estado (2002-2022)')
plt.show()