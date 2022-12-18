#!/bin/bash
set -ex 

###################################################################
# This script will get executed *once* the Docker container has 
# been built. Commands that need to be executed with all available
# tools and the filesystem mount enabled should be located here. 
###################################################################

# Warm up git index prior to display status in prompt else it will 
# be quite slow on every invocation of starship.

pip install -r requirements.txt

cd scraping
./main_runner.sh
./sync_to_s3.sh