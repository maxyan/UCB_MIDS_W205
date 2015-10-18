from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

lines = sc.textFile('file:///data/exercise1/hospital_compare/surveys_responses.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id hcahps_base_score hcahps_consistency_score'
surveys_responses = parts.map(lambda p:str(p[0])[1:-1]+','+str(p[31])[1:-1]+','+str(p[32])[1:-1])
surveys_responses.saveAsTextFile('file:///data/exercise1/surveys_responses')
