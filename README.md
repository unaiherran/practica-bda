## Brainstorming

El Ayuntamiento de Madrid proporciona datos de las estaciones de medida de la calidad del aire, pero en un formato poco amigable para realizar estudios de los mismos. Los datos no estan individualizados, sino que se sirven en medidas agregadas por dias. Es decir, no es posible obtener un dato concreto de medida de una estación a una hora, sino que hay que encontrar el archivo de ese mes, ver, las medidas que se realizaron ese día, aislarlo por horas , comprobar las medidas que se hicieron ese día y finalmente ver la medida

Así pues, planteo la siguiente idea:

* Obtener los datos de calidad del aire en Madrid
* Formatear los datos para alimentar un InfluxDB
* Presentar esos datos en un Grafana
* Por otro lado, alimentar esos datos a un Hadoop para poder realizar estudios de MapReduce para sacar medias por hora de las distintas medidas en distintas estaciones


## Arquitectura
Se establece la siguiente arquitectura:

https://docs.google.com/drawings/d/1tZDgS_LWooGMAurDQJDAo688y25-9PSn4WJjAsEnK_I/edit?usp=sharing

## Scrapper
Para obtener los datos se divide la tarea en dos:
* Por un lado hay que obtener los datos diarios. Según la documentación del API, los datos se actualizan entre el minuto 20 y 30 de cada hora, con lo que bastaría realizar un `CRON JOB (40 * * * *)` para que cada hora obtenga los datos

  El código sería similar a este:
https://colab.research.google.com/drive/1BlrmltxXA_TA4kw_t49jV74HExClrGjl#scrollTo=qIEPiWiQI0qI

  Tambien se puede ver en el Git en `scrapper_diario.py` (1) (No corre en local por usar librerias propias de Colab, pero con una pequeña adaptación funcionaría sin problemas) En el siguiente script se hacen estas modificaciones para demostrar que se entiende el funcionamiento de ambas

* Para adaptar el registo historico se ha escrito un script en local. Como sólo se va a ejecutar una vez,
se pueden cargar los archivos en el directorio `input` y ejecutar el script
 `python3 scrapper_historico.py $(ls input/)` (2) que dejará todos los archivos adaptados al formato
  elegido en `output`. Después se pueden subirá `gs://input_contaminacion`

## Hadoop

## InfluxBD
La arquitectura nos indica que la solución correcta sería montar una VM en Google Cloud Platform, pero para ahorrar costes enm la realización de la practuca, he optado por hacer una simulación en local con un docker container.
Para ejecutarlo, basta con tener docker instalado y ejecutar:

`docker run -d -p 8086:8086 -v $PWD:/var/lib/influxdb influxdb`

Esto montaría un InfluxDB que recibiría los datos desde los archivos generados en el scrapper (1 y 2). 

Debido a que la ingesta de datos de influxDB es a través de una API JSON he desarrolado el script: `preparacion_influxDB.py` que coge cada linea del csv generado con anterioridad y lo alimenta a InfluxDB. 

Para ejecutarlo en modo de prueba bastaría con dejar en `\output` los archivos csv que quieres almacenar en el influxDB y ejecutar el siguiente script `python3 preparacion_influxDB.py $(ls output/)`  (Tambien puedes ejecutar `python3 preparacion_influxDB.py file` para archivos individuales)

# Grafana
Usamos el mismo planteamiento para Grafana. Lo ideal sería montarlo en GCP, pero lo realizamos en local con un container.

`docker run -d --name=grafana -p 3000:3000 grafana/grafana`

Una vez montado lo configuramos de la siguiente manera:

