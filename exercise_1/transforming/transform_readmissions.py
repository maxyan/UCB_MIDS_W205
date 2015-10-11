from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

lines = sc.textFile('file:///data/exercise1/hospital_compare/readmissions.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id measure_id compare_to_national denominator score lower_estimate higher_estimate'
readmissions = parts.map(lambda p:(p[0],p[9], p[10],p[11],p[12], p[13], p[14])) # 'provider_id condition measure_id score sample'
readmissions.saveAsTextFile('file:///data/exercise1/readmissions')