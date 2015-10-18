from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

lines = sc.textFile('file:///data/exercise1/hospital_compare/readmissions.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id measure_id denominator score lower_estimate higher_estimate'
# 'provider_id measure_id denominator score lower_estimate higher_estimate'
readmissions = parts.map(lambda p:str(p[0])[1:-1]+','+str(p[9])[1:-1]+','+str(p[11])[1:-1]+','+str(p[12])[1:-1]+','+str(p[13])[1:-1]+','+str(p[14])[1:-1])
readmissions.saveAsTextFile('file:///data/exercise1/readmissions')
