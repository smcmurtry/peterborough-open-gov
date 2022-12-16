#!/bin/bash

export AWS_ACCESS_KEY_ID=${process.env.AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${process.env.AWS_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION=ca-central-1

aws s3 sync minutes s3://city-council-scraper/minutes
aws s3 cp generated_data/all_meeting_data.json s3://city-council-scraper/

# these commands were used to do the initial population of the s3 folder
# aws s3 cp ../playwright_output/output.2022.txt s3://city-council-scraper/playwright_output/
# aws s3 cp ../playwright_output/output.historical.txt s3://city-council-scraper/playwright_output/