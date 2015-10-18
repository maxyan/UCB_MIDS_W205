from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *

sc = SparkContext("local", "weblog app")
sqlContext=SQLContext(sc)
lines = sc.textFile('file:///data/exercise1/hospital_compare/hospitals.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id hospital_name state'
hospitals = parts.map(lambda p:str(p[0])[1:-1]+','+str(p[1])[1:-1]+','+str(p[4])[1:-1])
hospitals.saveAsTextFile('file:///data/exercise1/hospitals')

# Name or address sometimes contains ',', this is an example. Think about how to correct
seward = lines.filter(lambda x:"SEWARD" in x)

# Below deals with creating dataframes and tables - below is no longer relevant
# data_types = [StringType(), StringType(), StringType(), StringType(), StringType()]
# fields = [StructField(field_name, StringType(), True) for field_name in schema_string.split()]
# schema = StructType(fields)
# hospitals = parts.map(lambda p:(p[0],p[1], p[3],p[4],p[5]))
# schema_hospitals = sqlContext.createDataFrame(hospitals, schema)