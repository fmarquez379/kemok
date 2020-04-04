# -*- coding: utf-8 -*-
# Archivo main.py
# Autor Javier Paredes
# Fecha 2020-03-30
# Descripcion Este script permite recuperar la tasa de cambio
# de USD a Quetzales y almacenarlos en una base de datos sqlite.
# Tomando como referencia los valores publicados por el
# Banco de Guatemala en su pagina oficial.
# Recibe como parametro la fecha desde donde se desea actualizar
# la base de datos. Si se incluye el valor se tomara la fecha
# ingresada como fecha de inicio y la fecha de hoy como fecha fin,
# si ya existen valores desde esa fecha se reemplazaran en la bd
# si no se coloca el valor o su valor es la fecha de hoy simplemente
# se agregara el registro correspondiente a esa unica fecha en la bd.
# python main.py 2020-03-30

import sys
from datetime import date
from datetime import datetime
from lib.databases import DataBase
from lib.scrape import Scrape

cantArg = len(sys.argv)

if (cantArg > 1):
    try:
        fecha_ = str(sys.argv[1])
        fecha = datetime.strptime(fecha_, '%Y-%m-%d')
    except:
        fecha = date.today()
        print("\n No ha ingresado una fecha correcta...")
else:
    fecha = date.today()

datos = Scrape(fecha)
db = DataBase()

if __name__ == "__main__":
    cant = db.cant_registros_fecha(fecha)

    if (cant > 0):
        db.borrar_registros_fecha(fecha)

    datos.generar_valores()
    db.insertar(datos.valores)

    cant_ = db.cant_registros()
    print("Cantidad de registros totales: " + str(cant_))
    print("...")
