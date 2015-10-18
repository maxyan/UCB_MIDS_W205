from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

effective_care = sc.textFile('file:///data/exercise1/effective_care').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
procedure_care = effective_care.map(lambda p:(p[1][1], [p[0], p[1][2]]))
procedure_care_grouped = procedure_care.groupByKey()

def range_func(measures):
	scores = []
	for entry in measures:
		try:
			curr = int(entry[1])
		except:
			curr = None
		if curr is not None:
			scores.append(curr)
	if len(scores) < 1:
		return 0
	return max(scores) - min(scores)

measure_dates = sc.textFile('file:///data/exercise1/measure_dates').map(lambda l:l.encode().split(',')).map(lambda x: (x[1], x[0]))
procedure_score_range = procedure_care_grouped.map(lambda p:(p[0], range_func(p[1]))).join(measure_dates)
sorted_ranges = procedure_score_range.sortBy(lambda x:x[1], False)
top = sorted_ranges.take(10)
print(top)
