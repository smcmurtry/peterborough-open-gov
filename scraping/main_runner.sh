#!/bin/bash

python parse_scraped_data.py |
    --input_fpath=../playwright_output/output.txt \
    --output_fpath=generated_data/all_data_flat.json

python generate_all_meeting_data.py |
    --flat_data_fpath=generated_data/all_data_flat.json \
    --minutes_dir=minutes_new \
    --output_fpath=generated_data/all_meeting_data.json

python save_agendas |
    --flat_data_fpath=generated_data/all_data_flat.json
    --agenda_output_dir=agenda

python download_minutes.py |
    --agenda_input_dir=agenda \
    --minutes_output_dir=minutes_new

# need something to generate meeting_type_dict.json as well 