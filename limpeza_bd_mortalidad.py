import pandas as pd
import matplotlib.pyplot as plt


mortalidad_materna = pd.read_csv('mortalidad_materna.csv')

columnas_bd = ['ENTIDAD_RESIDENCIAD', 'EDAD_QUINQUENALD', 'CAUSA_CIE_4D', 'DERECHOHABIENCIAD', 'ANIO_DEFUNCION']

mortalidad = mortalidad_materna[columnas_bd]


mortalidad = mortalidad.rename(columns= {
    'ENTIDAD_RESIDENCIAD': 'estado',
    'EDAD_QUINQUENALD': 'rango_edad',
    'CAUSA_CIE_4D': 'tipo_aborto',
    'DERECHOHABIENCIAD': 'tipo_servicio_medico',
    'ANIO_DEFUNCION': 'defuncion',
    })
    

mortalidad_filtrada = mortalidad[mortalidad['tipo_aborto'].str.contains('aborto', case=False, na=False)]

agrupacion_anual = mortalidad_filtrada.groupby(['defuncion', 'tipo_aborto', 'tipo_servicio_medico']).agg({
    'estado': 'count',
    'tipo_servicio_medico': 'count'
}).rename(columns={'estado': 'conteo_por_estado',
                   'tipo_servicio_medico': 'conteo_servicio_medico'})


agrupacion_anual = agrupacion_anual.sort_values(by=('conteo_por_estado'), ascending=False).reset_index()

df_resultado = pd.merge(mortalidad_filtrada, agrupacion_anual, on=['defuncion', 'tipo_aborto', 'tipo_servicio_medico'], how='left')


# print(df_resultado)


columnas_exportar = ['estado', 'rango_edad', 'tipo_aborto', 'tipo_servicio_medico', 'defuncion']
df_resultado.to_csv('muertes_por_aborto.csv', columns=columnas_exportar, index=False)

# conteo_por_año = df_resultado.groupby('defuncion').size()

# df_resultado.groupby('defuncion')['conteo_por_estado'].sum().plot(kind='bar')
# plt.xlabel('Año')
# plt.ylabel('Número de casos')
# plt.title('Número de casos de aborto por año')
# plt.show()


# conteo_por_estado = df_resultado.groupby('estado').size()

# df_resultado.groupby('estado')['conteo_por_estado'].sum().plot(kind='bar')
# plt.xlabel('estado')
# plt.ylabel('Número de casos')
# plt.title('Número de casos de aborto por estado (2002-2022)')
# plt.show()


# servicio_medico = df_resultado.groupby('tipo_servicio_medico').size()

# df_resultado.groupby('tipo_servicio_medico')['conteo_servicio_medico'].sum().plot(kind='bar')
# plt.xlabel('tipo_derechohabiencia')
# plt.ylabel('cantidad')
# plt.title('DERECHOHABIENCIA (2002-2022)')
# plt.show()
