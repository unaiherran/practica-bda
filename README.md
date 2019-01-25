## Brainstorming

El Ayuntamiento de Madrid proporciona datos de las estaciones de medida de la calidad del aire, pero en un formato poco amigable para realizar estudios de los mismos. Los datos no estan individualizados, sino que se sirven en medidas agregadas por dias. Es decir, no es posible obtener un dato concreto de medida de una estación a una hora, sino que hay que encontrar el archivo de ese mes, ver, las medidas que se realizaron ese día, aislarlo por horas , comprobar las medidas que se hicieron ese día y finalmente ver la medida

Así pues, planteo la siguiente idea:

* Obtener los datos de calidad del aire en Madrid
* Formatear los datos para alimentar un InfluxDB
* Presentar esos datos en un Grafana
* Por otro lado, alimentar esos datos a un Hadoop para poder realizar estudios de MapReduce para sacar medias por hora de las distintas medidas en distintas estaciones
* Meter los datos del bucket en una base de datos (p.ej. HIVE)

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

Se monta un Hadoop en DataProc. Para las pruebas, se monta un cluster pequeño, un master y dos slaves, pero para un 
entorno real sería recomendable aumentar el número de nodos para que los trabajos no se eternicen.

La explicación de montado esta en:
https://colab.research.google.com/drive/1vJL-JOtqUpfI1OxszJ5U6z3iuI5-HOMG

## InfluxBD
La arquitectura nos indica que la solución correcta sería montar una VM en Google Cloud Platform, pero para ahorrar costes en la realización de la practuca, he optado por hacer una simulación en local con un docker container.
Para ejecutarlo, basta con tener docker instalado y ejecutar:

`docker run -d -p 8086:8086 -v $PWD:/var/lib/influxdb influxdb`

Esto montaría un InfluxDB que recibiría los datos desde los archivos generados en el scrapper (1 y 2). 

Debido a que la ingesta de datos de influxDB es a través de una API JSON he desarrolado el script: `preparacion_influxDB.py` que coge cada linea del csv generado con anterioridad y lo alimenta a InfluxDB. 

Para ejecutarlo en modo de prueba bastaría con dejar en `\output` los archivos csv que quieres almacenar en el influxDB y ejecutar el siguiente script `python3 preparacion_influxDB.py $(ls output/)`  (Tambien puedes ejecutar `python3 preparacion_influxDB.py file` para archivos individuales)

## Grafana
Usamos el mismo planteamiento para Grafana. Lo ideal sería montarlo en GCP, pero lo realizamos en local con un container.

`docker run -d --name=grafana -p 3000:3000 grafana/grafana`

Una vez montado lo configuramos de la siguiente manera:

*  Ir a `localhots:3000`
*  User: admin Password: admin
*  Add Data source
*  Seleccionar Influx
*  Configurar:

   -  Name: Calidad_aire
   -  Access: Browser
   -  URL: `localhost:8080`
   -  DB: calidad_aire
   -  U/P: root/root
   
* Con la conexión creada, añadir un dashboard nuevo e ir añadiendo paneles (Graph) y editando los mismos para obtener un panel similar al mostrado en `panel de mandos Grafana.png`

Una vez el panel está configurado, podemos importar nuevos datos a InfluxDB y vemos como se van actualizando los datos mostrados en los paneles. 


## Hive
Además de guardar los datos extraidos en un bucket en formato csv, se decide almacenar los datos en una base de datos HIVE, en una única tabla con los campos `FECHA_HORA,ESTACION,MAGNITUD,MEDIDA`

Se usa el ejemplo del docker suminsitrado en clase:


Componer el docker
```
docker-compose up -d --build
```
Copiar el archivo medidas.csv al interior del docker

```
docker cp medidas.csv a7ad3a292e3b:/opt/medidas.csv
```

Entrar en el docker y beeline
```
docker-compose exec hive-server bash
/opt/hive/bin/beeline -u jdbc:hive2://localhost:10000
```

ejecutar los siguientes comandos dentro de beehive
```
CREATE DATABASE calidad_aire;
USE calidad_aire;
```
Se crea una tabla temporal para la importacion, para ajustar el formato de los datetime ISO 8601 a TIMESTAMP
```
CREATE TABLE lecturas_tmp (fecha_hora STRING, estacion INT, magnitud STRING, medida FLOAT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ",";
LOAD DATA LOCAL INPATH '/opt/medidas.csv' INTO TABLE lecturas_tmp;

CREATE TABLE lecturas (fecha_hora TIMESTAMP, estacion INT, magnitud STRING, medida FLOAT);
INSERT INTO lecturas SELECT from_unixtime(unix_timestamp(regexp_replace(fecha_hora, 'T',' ')), 'yyyy-MM-dd HH:mm:ss') fecha_hora, estacion, magnitud, medida  from lecturas_tmp;

DROP TABLE lecturas_tmp;
```
Una vez realizado esto, se pueden realizar consultas SQL normales sobre la base de datos HIVE:
```
SELECT * FROM lecturas;
SELECT * FROM lecturas where magnitud="NOX";
```
