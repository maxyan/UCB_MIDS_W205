from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

effective_care = sc.textFile('file:///data/exercise1/effective_care').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
hospitals = sc.textFile('file:///data/exercise1/hospitals').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
readmissions = sc.textFile('file:///data/exercise1/readmissions').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))

# This function computes the average score given a key
def average_score(data):
	total = 0
	count = 0
	for entry in data:
		try:
			curr = int(entry)
		except:
			curr = None
		if curr:
			total += curr
			count += 1
	if count > 0:
		return float(total) / count
	return None


state_care = effective_care.join(hospitals).map(lambda p:(p[1][1][1], p[1][0][2]))
state_care_grouped = state_care.groupByKey()
state_care_scores = state_care_grouped.map(lambda p:(p[0], average_score(p[1]))).filter(lambda x:x[1] is not None)

highest_scores = state_care_scores.sortBy(lambda x:x[1], False)
lowest_scores = state_care_scores.sortBy(lambda x:x[1], True)

high_10 = highest_scores.take(10)
low_10 = lowest_scores.take(10)

print "Highest scores 10 states: \n"
print(high_10)

print "Lowest scores 10 states: \n"
print(low_10)
