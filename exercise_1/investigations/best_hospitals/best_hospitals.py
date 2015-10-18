from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

effective_care = sc.textFile('file:///data/exercise1/effective_care').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
readmissions = sc.textFile('file:///data/exercise1/readmissions').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
hospitals = sc.textFile('file:///data/exercise1/hospitals').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))

# This function computes the average score given a key
def average_care(measures, idx=2):
	total = 0
	count = 0
	for entry in measures:
		try:
			curr = int(entry[idx])
		except:
			curr = None
		if curr is not None:
			total += curr
			count += 1
	if count > 0:
		return float(total) / count
	return None

# compute average scores and sort them descendingly
care_grouped = effective_care.groupByKey() # group by key
care_scores = care_grouped.map(lambda p:(p[0], average_care(p[1]))).filter(lambda x:x[1] is not None)
care_scores_hospitals = care_scores.join(hospitals)
highest = care_scores_hospitals.sortBy(lambda x:x[1][0], False)
high_10 = highest.take(10)

lowest = care_scores_hospitals.sortBy(lambda x:x[1][0], True)
low_10 = lowest.take(10)

print "Highest scores 10 hospitals: \n"
print(high_10)

print "Lowest scores 10 hospitals: \n"
print(low_10)
