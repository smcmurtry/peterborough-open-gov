#!/bin/sh
set -e -x

cd playwright-scraper

# Install dependencies
npm install

# Install browsers
npx playwright install --with-deps chromium

# Run playwright test
npx playwright test tests/city-council.spec.ts

CURRENT_YEAR=$(date +'%Y')
aws s3 cp ../playwright-output/output.txt s3://${CITY_COUNCIL_SCRAPER_S3_BUCKET}/playwright-output/output.$CURRENT_YEAR.txt