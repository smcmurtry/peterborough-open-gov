import argparse
import os
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time


def download_minutes_from_agenda(agenda_input_dir, agenda_fname, minutes_output_dir):
    """
    This function takes an html agenda file and downloads the minutes pdfs.
    The minutes pdfs are for past meetings - they are approved in the current meeting.
    """
    meeting_type_str = agenda_fname.split(".")[1]
    f = open(f"{agenda_input_dir}/{agenda_fname}", "r")
    agenda_text = f.read()
    f.close()
    soup = BeautifulSoup(agenda_text, "html.parser")
    attachment_divs = soup.find_all("div", attrs={"class": "AgendaItemAttachment"})
    for attachment in attachment_divs:
        a = attachment.find("a")
        if not a:
            continue
        href = a.attrs["href"]
        url = f"https://pub-peterborough.escribemeetings.com/{href}"

        if "minutes" in a.text.lower():
            try:
                possible_date = a.text.split(" - ")[1].split(" ")[-1]
                date = datetime.strptime(possible_date, "%m-%d-%Y")
            except:
                try:
                    # filename like "06-03-2024 - Special Council Minutes.pdf"
                    possible_date = a.text.split(" - ")[0]
                    date = datetime.strptime(possible_date, "%m-%d-%Y")
                except:
                    continue
        else:
            possible_date = a.text[:10]
            if possible_date.count("-") != 2:
                continue

            if " " in possible_date:
                possible_short_date = possible_date.split(" ")[0]
                try:
                    date = datetime.strptime(possible_short_date, "%m-%d-%y")
                except:
                    continue
            else:
                try:
                    date = datetime.strptime(possible_date, "%m-%d-%Y")
                except ValueError:
                    try:
                        date = datetime.strptime(possible_date, "%Y-%m-%d")
                    except:
                        continue

        date_str = datetime.strftime(date, "%Y-%m-%d")
            
        new_fname = f"{date_str}.{meeting_type_str}.pdf"
        new_fpath = f"{minutes_output_dir}/{new_fname}"

        # do not overwrite
        if os.path.isfile(new_fpath):
            continue

        # download
        resp = requests.get(url)

        with open(new_fpath, "wb") as f:
            f.write(resp.content)
        print(f"download and save {new_fpath}")

        time.sleep(2)


def main(agenda_input_dir="python-etl-scraper/agenda", minutes_output_dir="python-etl-scraper/minutes"):
    agenda_fnames = os.listdir(agenda_input_dir)
    for n, agenda_fname in enumerate(agenda_fnames):
        print(n, end=", ")
        download_minutes_from_agenda(agenda_input_dir, agenda_fname, minutes_output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agenda_input_dir", help="input directory containing agendas")
    parser.add_argument("--minutes_output_dir", help="output directory containing minutes pdfs")
    args = parser.parse_args()
    if not args.agenda_input_dir or not args.minutes_output_dir:
        raise Exception("All arguments are required")

    main(agenda_input_dir=args.agenda_input_dir, minutes_output_dir=args.minutes_output_dir)