from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext("local", "weblog app")

def average_survey(entry):
	try:
		first = float(entry[0])
	except:
		first = None
	try:
		second = float(entry[1])
	except:
		second = None
		
	if first is None and second is None:
		return None
	elif second is None:
		return first
	elif first is None:
		return second
	else:
		return (first + second) / 2

def average_care(measures):
	total = 0
	count = 0
	for entry in measures:
		try:
			curr = int(entry[2])
		except:
			curr = None
		if curr is not None:
			total += curr
			count += 1
	if count > 0:
		return float(total) / count
	return None
	
surveys_responses = sc.textFile('file:///data/exercise1/surveys_responses').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
average_survey_score = surveys_responses.map(lambda x:(x[0], average_survey(x[1])))

effective_care = sc.textFile('file:///data/exercise1/effective_care').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
result = effective_care.groupByKey() # group by key
scores = result.map(lambda p:(p[0], average_care(p[1])))
joined_scores = scores.join(average_survey_score)
valid_joined_scores = joined_scores.filter(lambda x: x[1][0] is not None and x[1][1] is not None).map(lambda p:p[1])

all_scores = valid_joined_scores.collect()
care_scores = [entry[0] for entry in all_scores]
survey_scores = [entry[1] for entry in all_scores]

import numpy as np
print np.corrcoef(care_scores, survey_scores)
