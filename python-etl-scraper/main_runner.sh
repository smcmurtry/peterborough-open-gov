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

# I need to add some more code to run all pdfs after a certain date through the
# following program. Then probably another function to compile all the
# vote data files into one file
echo "Extracting vote data"
python extract_vote_data.py --minutes_input_dir minutes --votes_output_dir votes

echo "Compiling vote data"
python compile_vote_data.py --votes_input_dir votes --votes_output_fpath generated_data/all_vote_data.json