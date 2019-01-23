## Brainstorming

El Ayuntamiento de Madrid proporciona datos de las estaciones de medida de la calidad del aire, pero en un formato poco amigable para realizar estudios de los mismos. Los datos no estan individualizados, sino que se sirven en medidas agregadas por dias. Es decir, no es posible obtener un dato concreto de medida de una estación a una hora, sino que hay que encontrar el archivo de ese mes, ver, las medidas que se realizaron ese día, aislarlo por horas , comprobar las medidas que se hicieron ese día y finalmente ver la medida

Así pues, planteo la siguiente idea

*  Obtener los datos de calidad del aire en Madrid
*  Formatear los datos para alimentar un InfluxDB
* Presentar esos datos en un Grafana
* Por otro lado, alimentar esos datos a un Hadoop para poder realizar estudios de MapReduce para sacar medias por hora de las distintas medidas


## Arquitectura
