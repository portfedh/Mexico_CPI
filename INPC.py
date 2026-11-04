# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "pandas", "numpy", "truststore"]
# ///
# Programa para mostrar los valores del INPC de un periodo
# y calcular la inflación durante ese periodo.
# Autor: Pablo Cruz Lemini

import api_key
import requests
import truststore
import pandas as pd
# INEGI sends an incomplete certificate chain; use the OS trust store so
# requests can verify it (the bundled certifi store cannot).
truststore.inject_into_ssl()

# Spanish month names. A fixed list means the script does not depend on the
# es_ES locale being installed on the machine (it is missing on many systems).
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

class Inpc():
    # Variables
    token = api_key.token_inegi
    inpc = "910392"  # Serie INPC Mensual
    consulta = "false"  # Serie completa
    url = (
    "https://www.inegi.org.mx/app/api/indicadores/"
    + "desarrolladores/jsonxml/INDICATOR/"
    + inpc
    + "/es/00/"
    + consulta
    + "/BIE-BISE/2.0/"
    + token
    + "?type=json")

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
        status = None  # Stays None if we never get an HTTP response
        try:
            # timeout: do not wait forever if INEGI does not answer.
            response = requests.get(Inpc.url, timeout=30)
        except requests.exceptions.RequestException as error:
            # Print only the error type: the full message contains the URL,
            # and the URL contains the API token.
            df = None
            print("\n Error: No se pudo conectar con la API de INEGI")
            print(f"   Tipo de error: {type(error).__name__}")
            print("   -> Revisa tu conexion a internet, VPN o proxy")
            return False
        status = response.status_code
        if status == 200:
            content = response.json()
            data = content["Series"][0]["OBSERVATIONS"]
            # Se filtra el json
            # Se accesa el diccionario con los datos
            # Hacemos que la variable df sea global para poder accesarla despues
            df = pd.DataFrame(data)
            # Creamos un dataframe con la informacion
            df = df.drop(columns=["OBS_EXCEPTION",
                            "OBS_STATUS",
                            "OBS_SOURCE",
                            "OBS_NOTE",
                            "COBER_GEO",
                            ])
            # Eliminiamos las columnas que no necesitamos
            df.columns = ["Fecha", "INPC"]
            # Renombramos las columnas a Fecha e INPC
            df["INPC"] = df["INPC"].apply(lambda x: float(x))
            # Volvemos los datos del INPC floats en vez de strings
            df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y/%m")
            # Volvemos las fechas a formato de fecha
            df["Año"] = pd.DatetimeIndex(df["Fecha"]).year
            # Creamos las columna de Año
            df["Mes"] = df["Fecha"].dt.month.map(lambda m: MESES[m - 1])
            # Creamos las columna de Mes en español
            df = df.reindex(columns=["Fecha", "Año", "Mes", "INPC"])
            # Reordenamos las columnas
            df = df.set_index("Fecha")
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
                print("   -> Obten una nueva en: https://www.inegi.org.mx/servicios/api_indicadores.html")
            elif status == 403:
                print("   -> Acceso prohibido - verifica tu API key")
            elif status >= 500:
                print("   -> El servidor de INEGI esta temporalmente fuera de servicio")
            return False

    def print_last_value(self):
        print("\n Calculadora de Inflacion V1.2 04-Nov-26 \n")
        print("Ultimo Valor reportado por el INEGI: \n")
        if df is not None:
            print((df.iloc[[0], [0, 1, 2]]).to_string(index=False))
        else:
            print("   (No hay datos disponibles)")

    def ask_date(self, prompt):
        # Keep asking until the user types a valid yyyy-mm inside the data.
        first, last = df.index.min(), df.index.max()
        while True:
            print(prompt)
            text = input().strip()
            try:
                date = pd.to_datetime(text, format="%Y-%m")
            except ValueError:
                print(f"   Formato invalido: '{text}'. Usa yyyy-mm, por ejemplo 2024-01.")
                continue
            if not first <= date <= last:
                print(f"   Fuera de rango. Datos disponibles: "
                      f"{first:%Y-%m} a {last:%Y-%m}.")
                continue
            return date

    def get_dates(self):
        while True:
            self.start_date = self.ask_date("\n Fecha Inicial de Cálculo yyyy-mm: ")
            self.end_date = self.ask_date("Fecha Final de Cálculo yyyy-mm: ")
            if self.start_date <= self.end_date:
                break
            print("   La fecha inicial debe ser anterior o igual a la final.")

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
