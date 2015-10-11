from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

lines = sc.textFile('file:///data/exercise1/hospital_compare/measure_dates.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'measure_name measure_id measure_start_quarter measure_start_date measure_end_quarter measure_end_date'
measure_dates = parts.map(lambda p:(p[0],p[1], p[2],p[3],p[4], p[5])) # 'measure_name measure_id measure_start_quarter measure_start_date measure_end_quarter measure_end_date'
measure_dates.saveAsTextFile('file:///data/exercise1/measure_dates')
