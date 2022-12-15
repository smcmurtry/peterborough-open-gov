import argparse
import pandas as pd
import json
import os


def get_filename(url):
    if url == "None":
        return None
    return f"{url.split('=')[-1]}.pdf"


def get_fname(datetime_iso, meeting_type):
    """
    datetime_iso like: "2022-10-03T16:00:00" ",
    meeting_type like: "Accessibility Advisory Committee Meeting"
    """
    date = datetime_iso.split("T")[0]
    meeting_type = meeting_type.replace(" ", "-")
    meeting_type = meeting_type.replace(",","")
    return f"{date}.{meeting_type}"

def get_fill_minutes_fname(minutes_dir):
    def fill_minutes_fname(x):
        fname = f'{get_fname(x["datetime_iso"], x["meeting_type"])}.pdf'
        if not os.path.isfile(f"{minutes_dir}/{fname}"):
            return None
        return fname
    return fill_minutes_fname


def main(
    flat_data_fpath = "generated_data/all_data_flat.json",
    minutes_dir = "minutes",
    output_fpath = "generated_data/all_meeting_data.json"
    ):
    with open(flat_data_fpath, "r") as f:
        all_data_flat = json.load(f)
    
    all_data_flat_df = pd.DataFrame.from_records(all_data_flat)
    fill_minutes_fname = get_fill_minutes_fname(minutes_dir)
    all_data_flat_df["minutes_filename"] = all_data_flat_df.apply(fill_minutes_fname, axis=1)

    cols_of_interest = ["id", "meeting_type", "location", "datetime_iso", "agenda_url", "cancelled", "video_url", "minutes_filename"]

    all_data_flat_df[cols_of_interest].to_json(output_fpath, orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--flat_data_fpath_input", help="fpath for all_data_flat.json")
    parser.add_argument("--minutes_dir_input", help="directory to find minutes in")
    parser.add_argument("--output_fpath", help="fpath for generated all_meeting_data.json")
    args = parser.parse_args()
    if not args.flat_data_fpath_input or not args.minutes_dir_input or not args.output_fpath:
        raise Exception("All arguements are required")

    main(
        flat_data_fpath=args.flat_data_fpath_input,
        minutes_dir=args.minutes_dir_input,
        output_fpath=args.output_fpath
    )