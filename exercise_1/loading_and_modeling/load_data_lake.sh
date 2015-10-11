#!/bin/bash
mkdir temp_data
wget --output-document=hospital_data.zip 'https://data.medicare.gov/views/bg9k-emty/files/Nqcy71p9Ss2RSBWDmP77H1DQXcyacr2khotGbDHHW_s?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip'

cd temp_data
unzip ../hospital_data.zip

# Create new folder, move and rename files
mkdir /data/exercise1/
chmod 777 /data/exercise1/
mkdir /data/exercise1/hospital_compare
chmod 777 /data/exercise1/hospital_compare

cp "Hospital General Information.csv" hospitals.csv
cp "Timely and Effective Care - Hospital.csv" effective_care.csv
cp "Readmissions and Deaths - Hospital.csv" readmissions.csv
cp "Measure Dates.csv" measure_dates.csv
cp hvbp_hcahps_05_28_2015.csv surveys_responses.csv

# Remove the header
tail -n +2 hospitals.csv > /data/exercise1/hospital_compare/hospitals.csv
tail -n +2 effective_care.csv > /data/exercise1/hospital_compare/effective_care.csv
tail -n +2 readmissions.csv > /data/exercise1/hospital_compare/readmissions.csv
tail -n +2 measure_dates.csv > /data/exercise1/hospital_compare/measure_dates.csv
tail -n +2 surveys_responses.csv > /data/exercise1/hospital_compare/surveys_responses.csv


# Create directory in HDFS and put files into hdfs
sudo -u hdfs hdfs dfs -mkdir /user/w205/hospital_compare
sudo -u hdfs hdfs dfs -chmod 777 /user/w205/hospital_compare

sudo -u hdfs hdfs dfs -put effective_care.csv /user/w205/hospital_compare
sudo -u hdfs hdfs dfs -put hospitals.csv /user/w205/hospital_compare
sudo -u hdfs hdfs dfs -put measure_dates.csv /user/w205/hospital_compare
sudo -u hdfs hdfs dfs -put readmissions.csv /user/w205/hospital_compare
sudo -u hdfs hdfs dfs -put surveys_responses.csv /user/w205/hospital_compare