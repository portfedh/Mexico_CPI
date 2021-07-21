# Programa para mostrar los valores del INPC de un Periodo '
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
# Para mostrar el dataframe sin el indice   #Borrar si corre bien
# from IPython.display import display, HTML #Borrar si corre bien
# Para verificar que los inputs de fechas esten bien
from dateutil import parser

# Descargando la base de datos de INEGI
#######################################
# Mostrar los meses en Español
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

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
    url = ("https://www.inegi.org.mx/app/api/indicadores/"
           + "desarrolladores/jsonxml/INDICATOR/"
           + inpc+"/es/0700/"+consulta+"/BIE/2.0/"+token)
    # Se le tienen que pasar Headers
    # Se pasa como un Request con metodo Get
    # Se le solicita el codigo de respuesta al servidor.
    # status global para unittest
    global status
    response = requests.get(url)
    status = response.status_code

    # Si el estatus esta Ok armar el dataframe
    if status == 200:
        # Guarda la respuesta en formato Json en una variable
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
        df.drop(columns=['OBS_EXCEPTION',
                         'OBS_STATUS', 'OBS_SOURCE',
                         'OBS_NOTE', 'COBER_GEO'],
                inplace=True)
        df.columns = ['Fecha', 'INPC']
        df["INPC"] = df["INPC"].apply(lambda x: float(x))
        df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y/%m")
        df['Año'] = pd.DatetimeIndex(df['Fecha']).year
        df['Mes'] = pd.DatetimeIndex(df['Fecha'])\
            .month_name(locale='es_ES.UTF-8')
        df = df.reindex(columns=['Fecha', 'Año', 'Mes', 'INPC'])
        df.set_index("Fecha", inplace=True)
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
    ultimo_inpc = (df.iloc[[0]]).to_string(index=False)
    print(ultimo_inpc)
    # Para pruebas de inputs
    fecha_ultimo_inpc = (df.index[0])

    # Obteniendo la fecha inicial para filtrar tabla del INPC
    #########################################################
    print("\n Fecha Inicial de Cálculo yyyy-mm: ")
    start_date = input()

    # Prueba para ver que el input sea una fecha.
    try:
        isdate_test = bool(parser.parse(start_date))
    except Exception:
        isdate_test = False
    while isdate_test == False:
        print("\n ***** Fecha no valida, Intenta de nuevo *****")
        print("\n\n Fecha Inicial de Cálculo yyyy-mm: ")
        start_date = input()
        try:
            isdate_test = bool(parser.parse(start_date))
        except Exception:
            isdate_test = False

    # Prueba para evaluar
    # Si la fecha es posterior al inicio de la serie de INPC
    try:
        start_date = parser.parse(start_date)
        series_start_date = pd.to_datetime("1969-01-01")
        start_date_test = bool(start_date >= series_start_date)
    except Exception:
        start_date_test = False

    while start_date_test == False:
        print("\n ***** Fecha no valida. El INPC inicia en 1969-01-01 *****")
        print("\n ***** Intenta de nuevo *****")
        print("\n Fecha Inicial de Cálculo yyyy-mm: ")
        start_date = input()
        start_date = parser.parse(start_date)
        try:
            start_date_test = bool(start_date >= series_start_date)
        except Exception:
            start_date_test = False

    # Prueba para evaluar
    # Si la fecha es menor al ultimo valor del INPC
    try:
        last_date_test = bool(start_date <= fecha_ultimo_inpc)
    except Exception:
        last_date_test = False
    while last_date_test == False:
        print("\n ***** Fecha no valida. \
              La fecha elegida es posterior al \
              ultimo valor del INPC *****")
        print("\n ***** Intenta de nuevo *****")
        print("\n Fecha Inicial de Cálculo yyyy-mm: ")
        start_date = input()
        start_date = parser.parse(start_date)
        try:
            last_date_test = bool(start_date <= fecha_ultimo_inpc)
        except Exception:
            last_date_test = False

    # Obteniendo la fecha final para filtrar tabla del INPC
    #########################################################
    print("Fecha Final de Cálculo yyyy-mm: ")
    end_date = input()

    # Prueba para ver que el input sea una fecha.
    try:
        isdate_test = bool(parser.parse(end_date))
    except Exception:
        isdate_test = False
    while isdate_test == False:
        print("\n ***** Fecha no valida, Intenta de nuevo *****")
        print("\n\n Fecha Final de Cálculo yyyy-mm: ")
        end_date = input()
        try:
            isdate_test = bool(parser.parse(end_date))
        except Exception:
            isdate_test = False

    # Prueba para ver que la fecha final no sea anterior a la fecha inicial
    try:
        end_date = parser.parse(end_date)
        end_date_test = bool(end_date > start_date)
    except Exception:
        end_date_test = False
    while end_date_test == False:
        print("\n ***** Fecha no valida. \
                  La fecha final no puede ser anterior \
                  a la fecha inicial *****")
        print("\n ***** Intenta de nuevo *****")
        print("\n Fecha Final de Cálculo yyyy-mm: ")
        end_date = input()
        end_date = parser.parse(end_date)
        try:
            end_date_test = bool(end_date > start_date)
        except Exception:
            end_date_test = False

    # Prueba par ver que la fecha elegida sea menor al ultimo INPC
    try:
        last_date_test = bool(end_date <= fecha_ultimo_inpc)
    except Exception:
        last_date_test = False
    while last_date_test == False:
        print("\n ***** Fecha no valida. \
                  La fecha elegida es despues del ultimo valor del INPC *****")
        print("\n ***** Intenta de nuevo *****")
        print("\n Fecha Final de Cálculo yyyy-mm: ")
        end_date = input()
        end_date = parser.parse(end_date)
        try:
            last_date_test = bool(end_date <= fecha_ultimo_inpc)
        except Exception:
            last_date_test = False

    # Mostrando la informacion Filtrada
    ###############################################
    # Creamos un nuevo DataFrame solo con la info que nos interesa ver
    df2 = df.loc[end_date:start_date]

    # Calculamos la inflacion del Periodo
    start_value = df2['INPC'].values[-1]
    end_value = df2['INPC'].values[0]
    inflacion = ((end_value/start_value)-1)*100
    inflacion_redondeada = round(inflacion, 2)
    factor_ajuste = end_value/start_value
    factor_ajuste_truncado = round(factor_ajuste, 4)

    # Mostramos la informacion sin el indice
    print("\n")
    print(df2.to_string(index=False))

    # Mostramos la inflacion del periodo
    print("\nEl INPC Inicial del periodo es: "+str(start_value))
    print("El INPC Final del periodo es:: "+str(end_value))
    print("El Factor de ajuste es: "+str(factor_ajuste_truncado))
    print("La inflacion del periodo fue de: "+str(inflacion_redondeada)+"%\n")
