#!/usr/bin/python
#
# Scrapper de datos historicos de contaminacion
# parametro 1 nombre de archivo en input/


import sys
from datetime import datetime


import xml.etree.ElementTree as ET

DIR_SALIDA ='output/'

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

warning = 0
ficheros_creados = 0

for fichero in sys.argv[1:]:

    entrada = 'input/' + fichero

    tree = ET.parse(entrada)

    medidas = tree.getroot()

    # Inicio del archivo de salida

    out = 'FECHA_HORA,ESTACION,MAGNITUD,MEDIDA\n'

    for medida in medidas:
        anyo = int(medida.find("{http://bdca}ano").text)
        mes = int(medida.find("{http://bdca}mes").text)
        dia = int(medida.find("{http://bdca}dia").text)
        estacion = medida.find("{http://bdca}estacion").text
        magnitud = magnitudes[int(medida.find("{http://bdca}magnitud").text)]

        horas = {}
        for h in list(range(1,25)):
            h_xml = '{http://bdca}' + 'H' + str(h).zfill(2)
            try:
                horas[h] = medida.find(h_xml).text
            except AttributeError:
                print('Warning: dia {}/{} estacion: {} {} no existe'.format(dia, mes,estacion,h_xml))
                print('---')
                warning += 1

        for h, valor in horas.items():
            fecha = datetime(year=anyo, month=mes, day=dia, hour=h-1, minute=0, second=0)
            out += "{},{},{},{}\n".format(fecha.isoformat(), estacion, magnitud, valor)

    anyo_str = str(anyo).zfill(4)
    mes_str = str(mes).zfill(2)

    file_name = DIR_SALIDA + '{}{}-medidas.csv'.format(anyo_str, mes_str)

    with open(file_name, 'w') as f:
        f.write(out)
    ficheros_creados += 1

if warning:
    print ('Has tenido {} warnings'.format(warning))

print ('Se han creado {} ficheros en la carpeta output'.format(ficheros_creados))