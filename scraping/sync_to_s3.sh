#!/bin/bash

# these commands were used to do the initial population of the s3 folder
# aws s3 cp ../playwright_output/output.2022.txt s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/playwright_output/
# aws s3 cp ../playwright_output/output.historical.txt s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/playwright_output/

aws s3 sync minutes s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/minutes
aws s3 cp generated_data/all_meeting_data.json s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/