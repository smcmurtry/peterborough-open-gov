#!/bin/bash

python parse_scraped_data.py \
    --input_fpath ../playwright_output/output.txt \
    --output_fpath generated_data/all_data_flat.json

python save_agendas.py \
    --flat_data_fpath generated_data/all_data_flat.json \
    --agenda_output_dir agenda

python download_minutes.py agenda minutes_new

python generate_all_meeting_data.py generated_data/all_data_flat.json \
    minutes_new generated_data/all_meeting_data.json

# need something to generate meeting_type_dict.json as well 