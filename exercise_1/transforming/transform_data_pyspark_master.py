from pyspark.sql import SQLContext
from pyspark.sql.types import *

# Hospitals
sqlContext=SQLContext(sc)
lines = sc.textFile('file:///data/exercise1/hospital_compare/hospitals.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id hospital_name city state zipcode'
hospitals = parts.map(lambda p:(p[0],p[1], p[3],p[4],p[5])) # provider_id, hospital_name, city, state, zipcode
hospitals.saveAsTextFile('file:///data/exercise1/hospitals')

data_types = [StringType(), StringType(), StringType(), StringType(), StringType()]
fields = [StructField(field_name, StringType(), True) for field_name in schema_string.split()]
schema = StructType(fields)
hospitals = parts.map(lambda p:(p[0],p[1], p[3],p[4],p[5]))
schema_hospitals = sqlContext.createDataFrame(hospitals, schema)


# Effective Care
sqlContext=SQLContext(sc)
lines = sc.textFile('file:///data/exercise1/hospital_compare/effective_care.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id condition measure_id score sample'
effective_care = parts.map(lambda p:(p[0],p[8], p[9],p[11],p[12])) # 'provider_id condition measure_id score sample'
effective_care.saveAsTextFile('file:///data/exercise1/effective_care')

# Readmissions
lines = sc.textFile('file:///data/exercise1/hospital_compare/readmissions.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id measure_id compare_to_national denominator score lower_estimate higher_estimate'
readmissions = parts.map(lambda p:(p[0],p[9], p[10],p[11],p[12], p[13], p[14])) # 'provider_id condition measure_id score sample'
readmissions.saveAsTextFile('file:///data/exercise1/readmissions')

# Measures
lines = sc.textFile('file:///data/exercise1/hospital_compare/measure_dates.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'measure_name measure_id measure_start_quarter measure_start_date measure_end_quarter measure_end_date'
measure_dates = parts.map(lambda p:(p[0],p[1], p[2],p[3],p[4], p[5])) # 'measure_name measure_id measure_start_quarter measure_start_date measure_end_quarter measure_end_date'
measure_dates.saveAsTextFile('file:///data/exercise1/measure_dates')

# Responses
lines = sc.textFile('file:///data/exercise1/hospital_compare/surveys_responses.csv')
parts = lines.map(lambda l:l.split(','))
schema_string = 'provider_id hcahps_base_score hcahps_consistency_score'
surveys_responses = parts.map(lambda p:(p[0],p[31], p[32])) # 'provider_id hcahps_base_score hcahps_consistency_score'
surveys_responses.saveAsTextFile('file:///data/exercise1/surveys_responses')