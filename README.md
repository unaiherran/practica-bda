## Brainstorming

El Ayuntamiento de Madrid proporciona datos de las estaciones de medida de la calidad del aire, pero en un formato poco amigable para realizar estudios de los mismos. Los datos no estan individualizados, sino que se sirven en medidas agregadas por dias. Es decir, no es posible obtener un dato concreto de medida de una estación a una hora, sino que hay que encontrar el archivo de ese mes, ver, las medidas que se realizaron ese día, aislarlo por horas , comprobar las medidas que se hicieron ese día y finalmente ver la medida

Así pues, planteo la siguiente idea

*  Obtener los datos de calidad del aire en Madrid
*  Formatear los datos para alimentar un InfluxDB
* Presentar esos datos en un Grafana
* Por otro lado, alimentar esos datos a un Hadoop para poder realizar estudios de MapReduce para sacar medias por hora de las distintas medidas


## Arquitectura

## Scrapper
Para obtener los datos se divide la tarea en dos:
* Por un lado hay que obtener los datos diarios. Según la documentación del API, los datos se actualizan entre el minuto 20 y 30 de cada hora, con lo que bastaría realizar un CRON JOB (40 * * * *) para que cada hora obtenga los datos

  El código sería similar a este:
https://colab.research.google.com/drive/1BlrmltxXA_TA4kw_t49jV74HExClrGjl#scrollTo=qIEPiWiQI0qI

* Para adaptar el 


## Hadoop

## InfluxBD
hola
# Grafana
que tal
