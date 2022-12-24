import argparse
import os
import json

def main(
    votes_input_dir="votes",
    votes_output_fpath="generated_data/all_vote_data.json"
):
    votes_fnames = os.listdir(votes_input_dir)
    all_vote_data = {}
    for votes_fname in votes_fnames:
        id = ".".join(votes_fname.split(".")[:-1])
        with open(f"{votes_input_dir}/{votes_fname}", "r") as f:
            data = json.load(f)
            if data == []:
                continue
            all_vote_data[id] = data
    with open(votes_output_fpath, "w") as f:
        json.dump(all_vote_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--votes_input_dir", help="input directory containing vote data")
    parser.add_argument("--votes_output_fpath", help="output directory containing single vote data file")
    args = parser.parse_args()
    if not args.votes_input_dir or not args.votes_output_fpath:
        raise Exception("All arguments are required")

    main(votes_input_dir=args.votes_input_dir, votes_output_fpath=args.votes_output_fpath)