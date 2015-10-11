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