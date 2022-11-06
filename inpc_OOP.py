# Programa para mostrar los valores del INPC de un periodo
# y calcular la inflacion durante ese periodo.
# Autor: Pablo Cruz Lemini

import api_key
import locale
import requests
import pandas as pd
locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

class Inpc():
    # Variables
    token = api_key.token_inegi
    inpc = "628194"  # Serie INPC Mensual
    consulta = "false"  # Serie completa
    url = (
    "https://www.inegi.org.mx/app/api/indicadores/"
    + "desarrolladores/jsonxml/INDICATOR/"
    + inpc
    + "/es/0700/"
    + consulta
    + "/BIE/2.0/"
    + token)

    def __init__(self):
        self.serie_inegi()

    def test(self):
        

    def serie_inegi(self):
        global status # Global status for unitests
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            content = response.json()
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

    def print_intro(self):
        print("\n Calculadora de Inflacion V1. 17-Feb-21 \n")
        print("Ultimo Valor reportado por el INEGI: \n")
        print((df.iloc[[0], [0, 1, 2]]).to_string(index=False))

    def get_dates(self):
        print("\n Fecha Inicial de Cálculo yyyy-mm: ")
        self.start_date = pd.to_datetime(input())
        print("Fecha Final de Cálculo yyyy-mm: ")
        self.end_date = pd.to_datetime(input())

    def calculate_inflation(self):
        self.df2 = df.loc[self.end_date:self.start_date]
        self.start_value = df2["INPC"].values[-1]
        self.end_value = df2["INPC"].values[0]
        self.inflacion = ((end_value / start_value) - 1) * 100
        self.inflacion_redondeada = round(inflacion, 2)
        self.factor_ajuste = end_value / start_value
        self.factor_ajuste_truncado = round(factor_ajuste, 4)
    
    def print_information(self):
        print("\n")
        print(self.df2.to_string(index=False))
        print("\nEl INPC Inicial del periodo es: " + str(start_value))
        print("El INPC Final del periodo es:: " + str(end_value))
        print("El Factor de ajuste es: " + str(factor_ajuste_truncado))
        print(("La inflacion del periodo fue de: "
               + str(inflacion_redondeada)
               + "%\n"
               ))

if __name__ == '__main__':
    oInpc = Inpc()



