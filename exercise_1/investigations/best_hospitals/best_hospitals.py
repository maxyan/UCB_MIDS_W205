from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

effective_care = sc.textFile('file:///data/exercise1/effective_care').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
hospitals = sc.textFile('file:///data/exercise1/hospitals').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))

# Some exploration only
# 'provider_id condition measure_id score sample' - both score and sample can be "Not Available"
result = effective_care.groupByKey() # group by key

# This function computes the average score given a key
def average_score(measures, score_idx=2):
...     total = 0
...     count = 0
...     for entry in measures:
...             try:
...                     curr = int(entry[score_idx])
...             except:
...                     curr = None
...             if curr:
...                     total += curr
...                     count += 1
...     if count > 0:
...             return float(total) / count
...     return None

# compute average scores and sort them descendingly
scores = result.map(lambda p:(p[0], average_score(p[1])))
joined_scores = scores.join(hospitals_tuple)
sorted_scores = joined_scores.sortBy(lambda x:x[1][0], False)