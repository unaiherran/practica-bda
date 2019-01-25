CREATE TABLE lecturas_tmp (fecha_hora STRING, estacion INT, magnitud STRING, medida FLOAT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ",";
LOAD DATA LOCAL INPATH '/opt/medidas.csv' INTO TABLE lecturas_tmp;
CREATE TABLE lecturas (fecha_hora TIMESTAMP, estacion INT, magnitud STRING, medida FLOAT);

insert into lecturas SELECT from_unixtime(unix_timestamp(regexp_replace(fecha_hora, 'T',' ')), 'yyyy-MM-dd HH:mm:ss') fecha_hora, estacion, magnitud, medida  from lecturas_tmp;

drop table lecturas_tmp;
select * from lecturas;

