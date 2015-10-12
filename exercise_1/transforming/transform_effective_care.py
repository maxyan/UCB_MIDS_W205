from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

sqlContext=SQLContext(sc)
lines = sc.textFile('file:///data/exercise1/hospital_compare/effective_care.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id condition measure_id score sample'
effective_care = parts.map(lambda p:(p[0],p[8], p[9],p[11],p[12])) # 'provider_id condition measure_id score sample'
effective_care.saveAsTextFile('file:///data/exercise1/effective_care')

# Some exploration only
# 'provider_id condition measure_id score sample' - both score and sample can be "Not Available"
effective_care_tuple = parts.map(lambda p:(str(p[0])[1:-1],[str(p[8])[1:-1], str(p[9])[1:-1], str(p[11])[1:-1], str(p[12])[1:-1]]))

result = effective_care_tuple.groupByKey() # group by key
first_group = result.first()
list(first_group[1])