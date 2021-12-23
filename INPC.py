# Programa para mostrar los valores del INPC de un periodo
# y calcular la inflacion durante ese periodo.

# Imports del Programa
#######################
import api_key
# Para importar el token de INEGI
import locale
# Para mostrar las fechas en Español
import requests
# Para enviar HTTP requests usando Python
import pandas as pd
# Para transformar los datos en un DataFrame

# Descargando la base de datos de INEGI
#######################################
locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
# Mostrar los meses en Español
token = api_key.token_inegi
# Token de Consulta INEGI
inpc = "628194"  # INPC Mensual
# Serie de Consulta:
consulta = "false"
# Consulta de ultimo dato o serie completa:
#     Serie completa = "false"
#     Ultimo dato = "true"


# Funcion de Descarga de Datos:
###############################
def serie_inegi():
    # Al site de INEGI se le añaden los datos de consulta
    url = (
        "https://www.inegi.org.mx/app/api/indicadores/"
        + "desarrolladores/jsonxml/INDICATOR/"
        + inpc
        + "/es/0700/"
        + consulta
        + "/BIE/2.0/"
        + token
    )

    global status
    # Status global para unitest
    response = requests.get(url)
    # Se pasa como un request con metodo get
    status = response.status_code
    # Se le solicita el codigo de respuesta al servidor.

    if status == 200:
        # Si el estatus esta Ok crear el dataframe
        content = response.json()
        # Guarda la respuesta como una variable
        data = content["Series"][0]["OBSERVATIONS"]
        # Se filtra el json
        # Se accesa el diccionario con los datos
        global df
        # Hacemos que la variable df sea global para poder accesarla despues
        df = pd.DataFrame(data)
        # Creamos un dataframe con la informacion
        df.drop(columns=["OBS_EXCEPTION",
                         "OBS_STATUS",
                         "OBS_SOURCE",
                         "OBS_NOTE",
                         "COBER_GEO",
                         ],
                inplace=True,)
        # Eliminiamos las columnas que no necesitamos
        df.columns = ["Fecha", "INPC"]
        # Renombramos las columnas a Fecha e INPC
        df["INPC"] = df["INPC"].apply(lambda x: float(x))
        # Volvemos los datos del INPC floats en vez de strings
        df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y/%m")
        # Volvemos las fechas a formato de fecha
        df["Año"] = pd.DatetimeIndex(df["Fecha"]).year
        # Creamos las columna de Año
        df["Mes"] = (pd.DatetimeIndex(df["Fecha"])
                     .month_name(locale="es_ES.UTF-8"))
        # Creamos las columna de Mes en español
        df = df.reindex(columns=["Fecha", "Año", "Mes", "INPC"])
        # Reordenamos las columnas
        df.set_index("Fecha", inplace=True)
        # Volvemos la fecha la columna indice
        return df
        # Regresa el Dataframe
    else:
        # Si el estatus esta mal imprimir el Error en la consulta.
        print(status)


# Ejecutando la Solicitud de Descarga
#####################################
consulta_inpc = serie_inegi()

if __name__ == "__main__":

    # Obteniendo fechas para filtrar tabla del INPC
    #################################################
    print("\n Calculadora de Inflacion V1. 17-Feb-21 \n")
    print("Ultimo Valor reportado por el INEGI: \n")
    print((df.iloc[[0], [0, 1, 2]]).to_string(index=False))
    print("\n Fecha Inicial de Cálculo yyyy-mm: ")
    start_date = pd.to_datetime(input())
    print("Fecha Final de Cálculo yyyy-mm: ")
    end_date = pd.to_datetime(input())

    # Mostrando la informacion Filtrada
    ###################################
    df2 = df.loc[end_date:start_date]
    # Creamos un nuevo DataFrame solo con la info que nos interesa ver

    # Calculamos la inflacion del Periodo
    #####################################
    start_value = df2["INPC"].values[-1]
    end_value = df2["INPC"].values[0]
    inflacion = ((end_value / start_value) - 1) * 100
    inflacion_redondeada = round(inflacion, 2)
    factor_ajuste = end_value / start_value
    factor_ajuste_truncado = round(factor_ajuste, 4)

    # Mostramos la informacion sin el indice
    ########################################
    print("\n")
    print(df2.to_string(index=False))

    # Mostramos la inflacion del periodo
    ####################################
    print("\nEl INPC Inicial del periodo es: " + str(start_value))
    print("El INPC Final del periodo es:: " + str(end_value))
    print("El Factor de ajuste es: " + str(factor_ajuste_truncado))
    print(("La inflacion del periodo fue de: "
           + str(inflacion_redondeada)
           + "%\n"
           ))
