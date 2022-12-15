#!/bin/bash

python parse_scraped_data.py ../playwright_output/output.txt generated_data/all_data_flat.json

python save_agendas |
    --flat_data_fpath=generated_data/all_data_flat.json
    --agenda_output_dir=agenda

python download_minutes.py |
    --agenda_input_dir=agenda \
    --minutes_output_dir=minutes_new

python generate_all_meeting_data.py |
    --flat_data_fpath_input=generated_data/all_data_flat.json \
    --minutes_dir_input=minutes_new \
    --output_fpath=generated_data/all_meeting_data.json

# need something to generate meeting_type_dict.json as well 