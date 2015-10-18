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

def average_score(measures, idx=2):
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
	
surveys_responses = sc.textFile('file:///data/exercise1/surveys_responses').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
average_survey_score = surveys_responses.map(lambda x:(x[0], average_survey(x[1])))

effective_care = sc.textFile('file:///data/exercise1/effective_care').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
care_grouped = effective_care.groupByKey() # group by key
care_scores = care_grouped.map(lambda p:(p[0], average_score(p[1])))
joined_care_scores = care_scores.join(average_survey_score)
valid_joined_care_scores = joined_care_scores.filter(lambda x: x[1][0] is not None and x[1][1] is not None).map(lambda p:p[1])

all_scores = valid_joined_care_scores.collect()
care_scores = [entry[0] for entry in all_scores]
survey_scores = [entry[1] for entry in all_scores]

readmissions = sc.textFile('file:///data/exercise1/readmissions').map(lambda l:l.encode().split(',')).map(lambda x: (x[0], x[1:]))
readmissions_grouped = readmissions.groupByKey()
readmissions_scores = readmissions_grouped.map(lambda p:(p[0], average_score(p[1], 2)))
joined_readmin_scores = readmissions_scores.join(average_survey_score)
valid_joined_readmin_scores = joined_readmin_scores.filter(lambda x: x[1][0] is not None and x[1][1] is not None).map(lambda p:p[1])
all_readmin_survey_scores = valid_joined_readmin_scores.collect()
readmin_scores_list = [entry[0] for entry in all_readmin_survey_scores]
survey_scores_list = [entry[1] for entry in all_readmin_survey_scores]

import numpy as np
print '\n'
print 'Correlation between average effective_care scores and survey responses: \n'
print np.corrcoef(care_scores, survey_scores)

print '\n'
print 'Correlation between average readmission scores and survey responses: \n'
print np.corrcoef(readmin_scores_list, survey_scores_list)
