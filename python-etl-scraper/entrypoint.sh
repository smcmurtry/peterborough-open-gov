#!/bin/bash
set -ex 

###################################################################
# This script will get executed *once* the Docker container has 
# been built. Commands that need to be executed with all available
# tools and the filesystem mount enabled should be located here. 
###################################################################

cd python-etl-scraper

pip install -r requirements.txt

# these commands were used to do the initial population of the s3 folder
# aws s3 cp ../playwright-output/output.2022.txt s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/playwright-output/
# aws s3 cp ../playwright-output/output.historical.txt s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/playwright-output/

# get latest playwright output
aws s3 sync s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/playwright-output ../playwright-output 

./main_runner.sh

aws s3 sync minutes s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/minutes
aws s3 cp generated_data/all_meeting_data.json s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/