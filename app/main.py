import logging
import findspark

from params import conn_uri,path_trips_file,pipeline,table_db
from params import region_agg,decimal_size_lat_long,p1,p2,table_db_agg
from spark_configs import SparkClass
from trip_functions import trips, trips_boundingbox

findspark.init() 

spark = SparkClass().getSpark()

logging.info('Reading arguments')

logging.info('Choosen pipeline: %s', pipeline)

if pipeline == "ingest":
    logging.info('Starting pipeline')
    trips(spark=spark, path_trips_csv=path_trips_file,
            conn_uri=conn_uri,table_db=table_db,
             decimal_size_lat_long=decimal_size_lat_long)
elif pipeline == "avg_data":
    trips_boundingbox(spark = spark,conn_uri = conn_uri,
                        table_db_read=table_db,table_db_write=table_db_agg,
                        region=region_agg,p1=p1,p2=p2)
else:
    trips(spark=spark, path_trips_csv=path_trips_file,
            conn_uri=conn_uri,table_db=table_db,
             decimal_size_lat_long=decimal_size_lat_long)

    trips_boundingbox(spark = spark,conn_uri = conn_uri,
                        table_db_read=table_db,table_db_write=table_db_agg,
                        region=region_agg,p1=p1,p2=p2)