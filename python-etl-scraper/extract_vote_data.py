import argparse
import fitz
import json

def get_lines_from_doc(doc):
    lines = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:  # this block contains text
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if text:
                            bold = "bold" in s["font"].lower()
                            # s["size"] is always the same except for the title at the start
                            lines.append({"bold": bold, "text": text})
    return lines

def get_vote_data_from_lines(lines):
    vote_title = ""
    votes = []
    vote_obj = {}
    title_open = False
    for_open = False
    against_open = False
    for n, x in enumerate(lines):
        first_word = x["text"].split(" ")[0].lower()
        # 
        vote_data_in_progress = "title" in vote_obj.keys()
        if first_word in ["carried", "lost"] and vote_data_in_progress:
            for_open = False
            against_open = False
            # add the current vote data and clear
            vote_obj["carried"] = first_word == "carried"
            votes.append(vote_obj)
            vote_obj = {}

        if x["bold"]:
            title_open = True
            vote_title += x["text"] + " "
        if n+1 >= len(lines):
            # we have reached the end
            continue
        is_next_line_bold = lines[n+1]["bold"]
        next_line_text = lines[n+1]["text"]

        if title_open and is_next_line_bold:
            # the vote title continues
            continue
        if title_open and not is_next_line_bold and not next_line_text.lower()[:5] == "for (":
            # not a vote after all :(
            vote_title = ""
            continue
        if title_open and next_line_text.lower()[:5] == "for (":
            # we have found a vote!
            vote_obj["title"] = vote_title.strip() # strip trailing whitespace
            title_open = False
            continue
        if vote_data_in_progress and x["text"].lower()[:5] == "for (":
            for_open = True
            start_i = x["text"].index(")")
            vote_obj["for"] = x["text"][start_i+3:].strip() + " "
            continue
        if vote_data_in_progress and x["text"].lower()[:9] == "against (":
            for_open = False
            against_open = True
            start_i = x["text"].index(")")
            vote_obj["against"] = x["text"][start_i+3:].strip() + " "
            continue
        if vote_data_in_progress and for_open:
            vote_obj["for"] += x["text"].strip() + " "
        if vote_data_in_progress and against_open:
            vote_obj["against"] += x["text"].strip() + " "
    
    return votes

def clean_voter_str(voter_str):
    _voters = voter_str.split(",")
    voters = []
    for _voter in _voters:
        y = _voter.strip(" ")
        if y[:4] == "and ":
            y = y[4:]
        if len(y.split(" ")) == 1:
            # probably says "chair", not a voter but a title of the previous voter
            continue
        voters.append(y)
    return voters

def clean_data(votes):
    for vote_obj in votes:
        if "for" in vote_obj.keys():
            vote_obj["for"] = clean_voter_str(vote_obj["for"])
        else:
            vote_obj["for"] = []

        if "against" in vote_obj.keys():
            vote_obj["against"] = clean_voter_str(vote_obj["against"])
        else:
            vote_obj["against"] = []
    return votes


def main(
        minutes_fpath="../minutes/2022-12-06.City-Council-Meeting.pdf",
        output_fpath="../votes/2022-12-06.City-Council-Meeting.json"
    ):
    doc = fitz.open(minutes_fpath)
    lines = get_lines_from_doc(doc)
    _votes = get_vote_data_from_lines(lines)
    votes = clean_data(_votes)
    with open(output_fpath, "w") as f:
        json.dump(votes, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes_fpath", help="fpath to minutes pdf file")
    parser.add_argument("--output_fpath", help="fpath to output votes json file")
    args = parser.parse_args()
    if not args.minutes_fpath or not args.output_fpath:
        raise Exception("All arguments are required")
    main(args.minutes_fpath, args.output_fpath)