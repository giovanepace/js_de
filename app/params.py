path_trips_file = "/app_data/input/trips.csv"
conn_uri = "jdbc:postgresql://postgres:5432/challenge?user=admin&password=admin"
table_db = "trips"
table_db_agg = "trips_agg"
# pipeline = "ingest"
pipeline = "avg_data"
#Using size for to group the rows until 11.1m, see more on
# http://wiki.gis.com/wiki/index.php/Decimal_degrees
decimal_size_lat_long = 4
region_agg = "Hamburg"
p1 = {"lat":10.07,"long":53.60}
p2 = {"lat":9.85,"long":53.40}