import logging
from pyspark.sql.types import DoubleType, DecimalType
from pyspark.sql.functions import col, count, regexp_extract, to_timestamp, substring, weekofyear, sum, avg

def trips(spark, path_trips_csv, conn_uri, table_db, decimal_size_lat_long):

    df_trips = spark.read.format("csv").option("header","true").load(path_trips_csv)
    regex_lat_long =  r"([-]?[0-9]*[.][0-9]*)\s([-]?[0-9]*[.][0-9]*)"

    df_trips = df_trips.withColumn("datetime", to_timestamp(col("datetime"), "yyyy-MM-dd HH:mm:ss"))

    df_trips = df_trips.withColumn(
                "origin_lat",
                regexp_extract(col("origin_coord"), regex_lat_long, 1).cast(DecimalType(10,decimal_size_lat_long)),
            )
    df_trips = df_trips.withColumn(
                "origin_long",
                regexp_extract(col("origin_coord"), regex_lat_long, 2).cast(DecimalType(10,decimal_size_lat_long)),
            )
    df_trips = df_trips.withColumn(
                "destination_lat",
                regexp_extract(col("destination_coord"), regex_lat_long, 1).cast(DecimalType(10,decimal_size_lat_long)),
            )
    df_trips = df_trips.withColumn(
                "destination_long",
                regexp_extract(col("destination_coord"), regex_lat_long, 2).cast(DecimalType(10,decimal_size_lat_long)),
            )

    df_tripsagg = df_trips.groupBy(
            ["region",
            "origin_lat",
            "origin_long",
            "destination_lat",
            "destination_long",
            "datetime"]
            ).agg(count("datasource").alias("count"))
        
    print(df_tripsagg.show(10))

    df_tripsagg.write\
            .mode("overwrite")\
            .jdbc(conn_uri, table_db)

    logging.info('Data - trips - loaded')

def filter_coordinates(df, col_name, coordinates):
    return df.filter(
        (col(col_name) < max(*coordinates)) & (col(col_name) > min(*coordinates))
    )

def trips_boundingbox(spark,conn_uri,table_db_read,table_db_write,region,p1,p2):

    spark_table_df = spark.read.format("jdbc").option("url", conn_uri).option("dbtable", table_db_read).load()

    if region != None:
        spark_table_df = spark_table_df.filter(col("region") == region)
    if (p1 != None) and (p2 != None):
        spark_table_df = filter_coordinates(spark_table_df, "origin_lat", [p1["lat"], p2["lat"]])
        spark_table_df = filter_coordinates(spark_table_df, "destination_lat", [p1["lat"], p2["lat"]])
        spark_table_df = filter_coordinates(spark_table_df, "origin_long", [p1["long"], p2["long"]])
        spark_table_df = filter_coordinates(spark_table_df, "destination_long", [p1["long"], p2["long"]])

    spark_table_df = spark_table_df.groupBy(weekofyear(("datetime"))).agg(
            sum("count").alias("trips_per_week")
        )
    spark_table_df = spark_table_df.agg(avg("trips_per_week").alias("weekly_avg_trips"))

    spark_table_df.write\
            .mode("overwrite")\
            .jdbc(conn_uri, table_db_write)
    
    logging.info('Data - trips in bounding box - loaded')