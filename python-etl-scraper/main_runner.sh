#!/bin/bash

echo "Parsing scraped data"
python parse_scraped_data.py \
    --input_dir ../playwright-output \
    --output_fpath generated_data/all_data_flat.json

echo "Saving agendas"
python save_agendas.py \
    --flat_data_fpath generated_data/all_data_flat.json \
    --agenda_output_dir agenda

echo "Downloading minutes"
python download_minutes.py \
    --agenda_input_dir agenda \
    --minutes_output_dir minutes

echo "Generating all_meeting_data.json"
python generate_all_meeting_data.py \
    --flat_data_fpath_input generated_data/all_data_flat.json \
    --minutes_dir_input minutes \
    --output_fpath generated_data/all_meeting_data.json
