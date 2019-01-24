#!/usr/bin/python
#
# Prepara los archivos que hay en output y los suministra via JSON y el cliente de InfluxDB a la base de datos que
# corre en un docker
#

from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep
import sys
import csv

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'calidad_aire')

client.create_database('calidad_aire')


for fichero in sys.argv[1:]:

    entrada = 'output/' + fichero

    f = open(entrada, 'r')

    countdr = csv.DictReader(f)
    total_rows = 0
    for row in countdr:
        total_rows += 1

    f.seek(0)

    reader = csv.DictReader(f, fieldnames=('FECHA_HORA','ESTACION','MAGNITUD','MEDIDA'))


    # Saltarse la primera fila con los encabezados)
    next(reader)

    # Recorrer el archivo
    n = 0

    for row in reader:

        json_body = [
            {
                "measurement": row['MAGNITUD'],
                "tags": {
                      "provider": "Ayuntamiento de Madrid",
                      },
                "time": row['FECHA_HORA'],
                "fields": {
                    "estacion": row['ESTACION'],
                    "value":float(row['MEDIDA'])
                }

            }
        ]

        client.write_points(json_body)
        n += 1

        if not(n % 1000): print('{}/{} Valores añadidos'.format(n, total_rows ))

    print('{} entradas añadidas del fichero {}'.format(n, entrada))


#
#
# while True:
#     json_body = [
#          {
#              "measurement": "btc_price_usd",
#              "tags": {
#                  "provider": "bitfinex",
#                  },
#              "time": now,
#              "fields": {
#                  "value": float(current_price)
#                  }
#              }
#          ]
#
#     client.write_points(json_body)
#     sleep(5)
