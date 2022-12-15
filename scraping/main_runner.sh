#!/bin/bash

python parse_scraped_data.py ../playwright_output/output.txt generated_data/all_data_flat.json

python save_agendas.py generated_data/all_data_flat.json agenda

python download_minutes.py agenda minutes_new

python generate_all_meeting_data.py |
    --flat_data_fpath_input=generated_data/all_data_flat.json \
    --minutes_dir_input=minutes_new \
    --output_fpath=generated_data/all_meeting_data.json

# need something to generate meeting_type_dict.json as well 