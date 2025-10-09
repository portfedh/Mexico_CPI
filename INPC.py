# Programa para mostrar los valores del INPC de un periodo
# y calcular la inflación durante ese periodo.
# Autor: Pablo Cruz Lemini

import api_key
import locale
import requests
import pandas as pd
locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

class Inpc():
    # Variables
    token = api_key.token_inegi
    inpc = "910392"  # Serie INPC Mensual
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
        if not self.get_inpc_data():
            print("\n El programa no puede continuar sin datos del INEGI.\n")
            return
        self.print_last_value()
        self.get_dates()
        self.calculate_inflation()
        self.print_information()


    def get_inpc_data(self):
        global status # Global status for unit tests
        global df # Global dataframe
        response = requests.get(Inpc.url)
        status = response.status_code
        if status == 200:
            content = response.json()
            data = content["Series"][0]["OBSERVATIONS"]
            # Se filtra el json
            # Se accesa el diccionario con los datos
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
            return True
            # Regresa True si fue exitoso
        else:
            # Si el estatus esta mal imprimir el Error en la consulta.
            df = None
            print(f"\n Error: No se pudo conectar con la API de INEGI")
            print(f"   Codigo de estado HTTP: {status}")
            if status == 401:
                print("   -> Tu API key esta invalida o expirada")
                print("   -> Obten una nueva en: http://en.www.inegi.org.mx/app/api/denue/v1/tokenVerify.aspx")
            elif status == 403:
                print("   -> Acceso prohibido - verifica tu API key")
            elif status >= 500:
                print("   -> El servidor de INEGI esta temporalmente fuera de servicio")
            return False

    def print_last_value(self):
        print("\n Calculadora de Inflacion V1.1 09-Oct-25 \n")
        print("Ultimo Valor reportado por el INEGI: \n")
        if df is not None:
            print((df.iloc[[0], [0, 1, 2]]).to_string(index=False))
        else:
            print("   (No hay datos disponibles)")

    def get_dates(self):
        print("\n Fecha Inicial de Cálculo yyyy-mm: ")
        self.start_date = pd.to_datetime(input())
        print("Fecha Final de Cálculo yyyy-mm: ")
        self.end_date = pd.to_datetime(input())

    def calculate_inflation(self):
        self.df2 = df.loc[self.end_date:self.start_date]
        self.start_value = self.df2["INPC"].values[-1]
        self.end_value = self.df2["INPC"].values[0]
        self.inflacion = ((self.end_value / self.start_value) - 1) * 100
        self.inflacion_redondeada = round(self.inflacion, 2)
        self.factor_ajuste = self.end_value / self.start_value
        self.factor_ajuste_truncado = round(self.factor_ajuste, 4)
    
    def print_information(self):
        print("\n")
        print(self.df2.to_string(index=False))
        print("\nEl INPC Inicial del periodo es: " + str(self.start_value))
        print("El INPC Final del periodo es:: " + str(self.end_value))
        print("El Factor de ajuste es: " + str(self.factor_ajuste_truncado))
        print(("La inflacion del periodo fue de: "
               + str(self.inflacion_redondeada)
               + "%\n"
               ))

if __name__ == '__main__':
    oInpc = Inpc()
