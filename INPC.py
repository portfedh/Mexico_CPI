# Programa para mostrar los valores del INPC de un Periodo
# y Calcular la inflacion durante ese periodo. 

# Imports del Programa
#######################
# Para importar el token de Banxico
import api_key
# Para sacar las enviroment variables
# import os # Uncomment si se usa 
# Para hacer que los meses se muestren en Español
import locale
# Para enviar HTTP requests usando Python
import requests
# Para transformar los datos en un DataFrame
import pandas as pd
# Para procesar datos
import numpy as np
# Para mostrar el dataframe sin el indice
from IPython.display import display, HTML

# Descargando la base de datos de INEGI
#######################################
# Mostrar los meses en Español
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

# Token de Consulta INEGI
token = api_key.token_inegi
# alternativa si quieres poner el token directamente en un solo archivo
# token = "token_aqui"
# alternativa si quieres poner el token en las OS variables
# token = os.environ.get("token_inegi")

# Serie de Consulta: 
inpc = "628194"  # INPC Mensual

# Consulta de Ultimo dato o serie completa:
    # - Serie completa = "false"
    # - Ultimo dato = "true"
consulta = "false"

# Funcion de Descarga:
def serie_inegi():
    # Al site de INEGI se le añaden los datos de consulta
    url = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/"+inpc+"/es/0700/"+consulta+"/BIE/2.0/"+token

    # Se le tienen que pasar Headers
    # Se pasa como un Request con metodo Get
    # Se le solicita el codigo de respuesta al servidor. 
    # status global para unittest
    global status
    response = requests.get(url) 
    status = response.status_code
    
    # Si el estatus esta Ok armar el dataframe
    if status == 200:
        # Si el codigo es correcto guarda la respuesta en formato Json en una variable
        content = response.json()
        
        # Pasamos las llaves en el Json para crear el dataframe. 
        data = content["Series"][0]["OBSERVATIONS"]

        # Hacemos que la variable df sea global para poder accesarla despues
        # Creamos con la serie un dataframe df
        # Eliminiamos las columnas que no necesitamos
        # Renombramos las columnas a Fecha e INPC
        # Volvemos los datos del INPC floats en vez de strings
        # Volvemos las fechas a formato de fecha
        # Creamos las columna de Año 
        # Creamos las columna de Mes en español
        # Reordenamos las columnas
        # Regresa el Dataframe
        # Volvemos la fecha la columna indice
        global df
        df = pd.DataFrame(data)
        df.drop(columns=['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE', 'OBS_NOTE', 'COBER_GEO'], inplace=True)
        df.columns = ['Fecha', 'INPC']
        df["INPC"] = df["INPC"].apply(lambda x: float(x))
        df["Fecha"] = pd.to_datetime(df["Fecha"], format = "%Y/%m")
        df['Año'] = pd.DatetimeIndex(df['Fecha']).year
        df['Mes'] = pd.DatetimeIndex(df['Fecha']).month_name(locale='es_ES.UTF-8')
        df = df.reindex(columns= ['Fecha','Año', 'Mes','INPC'])
        df.set_index("Fecha", inplace = True)
        return df
    
    # Si el estatus esta mal imprimir el Error en la consulta.
    else:
         print(status)
            
# Llamamos la funcion
consulta_inpc = serie_inegi()

if __name__ == '__main__':

    # Obteniendo fechas para filtrar tabla del INPC
    #################################################
    print("\n Calculadora de Inflacion V1. 17-Feb-21 \n")
    print("Ultimo Valor reportado por el INEGI: \n")
    print((df.iloc[[0],[0,1,2]]).to_string(index=False))
    print("\n Fecha Inicial de Cálculo yyyy-mm: ")
    start_date = input()
    print("Fecha Final de Cálculo yyyy-mm: ")
    end_date = input()

    # Mostrando la informacion Filtrada
    ###############################################
    # Creamos un nuevo DataFrame solo con la info que nos interesa ver
    df2 = df.loc[end_date:start_date]

    # Calculamos la inflacion del Periodo
    start_value = df2['INPC'].values[-1]
    end_value   = df2['INPC'].values[0]
    inflacion = ((end_value/start_value)-1)*100
    inflacion_redondeada = round(inflacion,2)
    factor_ajuste = end_value/start_value
    factor_ajuste_truncado = round(factor_ajuste,4)

    # Mostramos la informacion sin el indice
    print("\n")
    print(df2.to_string(index=False))

    # Mostramos la inflacion del periodo
    print("\nEl INPC Inicial del periodo es: "+str(start_value))
    print("El INPC Final del periodo es:: "+str(end_value))
    print("El Factor de ajuste es: "+str(factor_ajuste_truncado))
    print("La inflacion del periodo fue de: "+str(inflacion_redondeada)+"%\n")
