from pyspark.sql import SparkSession

class SparkClass:
    def getSpark(self):
        return SparkSession.builder\
                .getOrCreate()