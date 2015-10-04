#wget --output-document=hospital_data.zip https://data.medicare.gov/views/bg9k-emty/files/Nqcy71p9Ss2RSBWDmP77H1DQXcyacr2khotGbDHHW_s?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip

#unzip hospital_data.zip

# Create new folder, move and rename files
mkdir hospital_compare

cp "Hospital General Information.csv" hospital_compare/hospitals.csv
cp "Timely and Effective Care - Hospital.csv" hospital_compare/effective_care.csv
cp "Readmissions and Deaths - Hospital.csv" hospital_compare/readmissions.csv
cp "Measure Dates.csv" hospital_compare/measure_dates.csv
cp hvbp_hcahps_05_28_2015.csv hospital_compare/surveys_responses.csv

# Remove the header
tail -n +2 hospital_compare/hospitals.csv > hospital_compare/hospitals.csv
tail -n +2 hospital_compare/effective_care.csv > hospital_compare/effective_care.csv
tail -n +2 hospital_compare/readmissions.csv > hospital_compare/readmissions.csv
tail -n +2 hospital_compare/measure_dates.csv > hospital_compare/measure_dates.csv
tail -n +2 hospital_compare/surveys_responses.csv > hospital_compare/surveys_responses.csv

