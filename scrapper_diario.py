from googleapiclient.http import MediaFileUpload
from datetime import datetime

from google.colab import files

import requests
import xml.etree.ElementTree as ET


# Variables para el crawler
headers = {'User-Agent': 'Crawler Unai Herran'}
ADDRESS = 'http://www.mambiente.munimadrid.es/opendata/horario.xml'

# diccionario de magnitudes

magnitudes = {1:'SO2',
            6: 'CO',
            7: 'NO',
            8: 'NO2',
            9: 'PM2.5' ,
            10: 'PM10',
            12: 'NOX',
            14: 'O3',
            20: 'TOL',
            30: 'BEN',
            35: 'EBE',
            37: 'MXY',
            38: 'PXY',
            39: 'OXY',
            42: 'TCH',
            43: 'CH4',
            44: 'NMHC'}


# Una vez establecidas las variables de entorno se realiza la petición

response = requests.get(ADDRESS, headers)
tree = ET.ElementTree(ET.fromstring(response.content))
root = tree.getroot()

# Limpieza de XML

inicio = b'<?xml version="1.0" encoding="utf-8"?>\n<Datos '
fin = response.content[65:]

cont = inicio + fin

# Se establece un arbol XML en medidas

medidas = ET.fromstring(cont)

# Inicio del archivo de salida

out = 'FECHA_HORA,ESTACION,MAGNITUD,MEDIDA\n'

for medida in medidas:
  anyo = int(medida.find("ano").text)
  mes = int(medida.find("mes").text)
  dia = int(medida.find("dia").text)
  estacion = medida.find("estacion").text
  magnitud = magnitudes[int(medida.find("magnitud").text)]

  horas = {}
  for h in list(range(1,25)):
    h_xml = 'H' + str(h).zfill(2)
    horas[h] = medida.find(h_xml).text

  for h, valor in horas.items():
    fecha = datetime(year = anyo, month = mes, day = dia, hour = h-1, minute=0,second = 0)
    out += "{},{},{},{}\n".format(fecha.isoformat(), estacion, magnitud, valor)


with open('medidas.csv', 'w') as f:
  f.write(out)


project_id = 'contaminacionmadrid'

# Authenticate to GCS.
from google.colab import auth
auth.authenticate_user()

# Create the service client.
from googleapiclient.discovery import build
gcs_service = build('storage', 'v1')

bucket_name = 'input_contaminacion'


# esto sirve para crear el bucket en caso de que no exista
# ------------
# body = {
#  'name': bucket_name,
#  # For a full list of locations, see:
#  # https://cloud.google.com/storage/docs/bucket-locations
#  'location': 'us',
# }

# gcs_service.buckets().insert(project=project_id, body=body).execute()
# ------


media = MediaFileUpload('medidas.csv',
                        mimetype='text/csv',
                        resumable=True)

anyo_str = str(anyo).zfill(4)
mes_str = str(mes).zfill(2)
dia_str = str(dia).zfill(2)

name = "{}{}{}-medidas".format(anyo_str, mes_str, dia_str)

request = gcs_service.objects().insert(bucket=bucket_name,
                                       name=name,
                                       media_body=media)

response = None
while response is None:
  # _ is a placeholder for a progress object that we ignore.
  # (Our file is small, so we skip reporting progress.)
  _, response = request.next_chunk()

