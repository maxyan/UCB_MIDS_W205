from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

lines = sc.textFile('file:///data/exercise1/hospital_compare/measure_dates.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'measure_name measure_id'
measure_dates = parts.map(lambda p:str(p[0])[1:-1]+','+str(p[1])[1:-1])
measure_dates.saveAsTextFile('file:///data/exercise1/measure_dates')
