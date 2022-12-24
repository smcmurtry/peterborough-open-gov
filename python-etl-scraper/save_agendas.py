import argparse
import requests
import os
import time
import json

from generate_all_meeting_data import get_fname

def save_agenda(meeting, agenda_dir, overwrite=False) -> None:
    """
    Do not request if we already have it saved.
    """
    fname = get_fname(meeting["datetime_iso"], meeting["meeting_type"])
    fpath = f"{agenda_dir}/{fname}.html"
    # check if file exists
    if not overwrite and os.path.isfile(fpath):
        return
    resp = requests.get(meeting["agenda_url"])
    with open(fpath, "w") as f:
        f.write(resp.text)
    time.sleep(2)
    return


def main(
    flat_data_fpath="generated_data/all_data_flat.json",
    agenda_output_dir="agenda"
):
    with open(flat_data_fpath, "r") as f:
        all_data_flat = json.load(f)
        for n, meeting in enumerate(all_data_flat):
            print(n, end=", ")
            save_agenda(meeting, agenda_output_dir)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--flat_data_fpath", help="input fpath for all_data_flat.json")
    parser.add_argument("--agenda_output_dir", help="output directory for agendas")
    args = parser.parse_args()
    if not args.flat_data_fpath or not args.agenda_output_dir:
        raise Exception("All arguments are required")
    main(flat_data_fpath=args.flat_data_fpath, agenda_output_dir=args.agenda_output_dir)