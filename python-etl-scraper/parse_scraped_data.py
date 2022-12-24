import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.parse import parse_qs
from urllib import parse
import pandas as pd
from typing import List
from my_types import Link, Meeting
import os


def parse_meeting_date(datetime_str: str) -> str:
    "datetime_str like Monday, 'December 06, 2021 @  6:30 PM'"
    string_format = "%A, %B %d, %Y @ %I:%M %p"
    parsed = datetime.strptime(datetime_str, string_format)
    return parsed.isoformat()


def parse_link_soup(link_soup) -> Link:
    link: Link = {}  
    link["aria_label"] = link_soup.attrs["aria-label"]
    link["href"] = link_soup.attrs["href"]
    link["link_text"] = link_soup.text.strip()
    link["url"] = "https://pub-peterborough.escribemeetings.com/" + link["href"]
    return link


def parse_meeting_soup(meeting_soup) -> Meeting:
    meeting: Meeting = {}
    meeting["meeting_type"] = meeting_soup.find(
        "div", {"class": "meeting-title"}
    ).text.strip()
    datetime_str = meeting_soup.find("div", {"class": "meeting-date"}).text.strip()
    meeting["location"] = meeting_soup.find(
        "div", {"class": "startLocation"}
    ).text.strip()
    meeting["datetime_iso"] = parse_meeting_date(datetime_str)
    link_soup_list = meeting_soup.find_all("a", {"class": "link"})
    meeting["links"] = []
    for link_soup in link_soup_list:
        link = parse_link_soup(link_soup)
        meeting["links"].append(link)
    return meeting


def parse_playwright_output(playwright_output) -> List[Meeting]:
    soup = BeautifulSoup(playwright_output, "html.parser")
    all_meetings_of_type_2021 = soup.find_all("div", {"class": "meeting-header"})
    parsed_meetings = []
    for meeting_soup in all_meetings_of_type_2021:
        meeting = parse_meeting_soup(meeting_soup)
        parsed_meetings.append(meeting)
    return parsed_meetings


def get_minutes_url(links, file_type="html"):
    # if minutes is in aria_label.lower() then it is the minutes
    # link text gives file type
    "file_type in ['html', 'pdf']"
    for x in links:
        if "minutes" not in x["aria_label"].lower():
            continue
        if file_type == x["link_text"].lower():
            return x["url"]
        return ""
    return ""


def is_cancelled(links):
    for x in links:
        if "cancellation" in x["link_text"].lower():
            return True
    return False


def get_video_url(links):
    for x in links:
        if x["link_text"].lower() == "video":
            return x["url"]
    return ""


def get_id(url: str) -> str:
    "Get the meeting id used by the external site"
    query_dict = dict(parse.parse_qs(parse.urlsplit(url).query))
    if "Id" not in query_dict:
        # these seem to be urls for cancellation notices
        # @todo: fix my scraping program since cancelled meetings should still have agendas
        return "blah"
    return query_dict["Id"][0]


def get_agenda_url(x):
    try:
        return x[0]["url"]
    except:
        return ""


def assemble_dataframe_and_save(all_data):
    df = pd.DataFrame.from_dict(all_data)
    df["agenda_url"] = df["links"].map(get_agenda_url)
    df["minutes_html_url"] = df["links"].map(lambda x: get_minutes_url(x, "html"))
    df["minutes_pdf_url"] = df["links"].map(lambda x: get_minutes_url(x, "pdf"))
    df["cancelled"] = df["links"].map(is_cancelled)
    df["video_url"] = df["links"].map(get_video_url)
    df["id"] = df["agenda_url"].map(lambda url: get_id(url))
    cols_of_interest = [
        "id",
        "meeting_type",
        "location",
        "datetime_iso",
        "agenda_url",
        "minutes_html_url",
        "minutes_pdf_url",
        "cancelled",
        "video_url",
    ]

    # all_meeting_types = list(set(df["meeting_type"]))
    # with open("generated_data/all_meeting_types.json", "w") as f:
    #     json.dump(all_meeting_types, f)

    return df[cols_of_interest]


def get_unique_meetings(non_unique_meetings: List[Meeting]) -> List[Meeting]:
    _meeting_dict = {}
    for meeting in non_unique_meetings:
        key = f"{meeting['meeting_type']}-{meeting['datetime_iso']}"
        _meeting_dict[key] = meeting
    return list(_meeting_dict.values())


def main(
        input_dir = "../playwright-output",
        output_fpath = "generated_data/all_data_flat.json"
    ):
    """
    This takes the scraped playwright data as input and writes the meeting
    data to file. The meeting data is of type: List[Meeting]
    """
    output_fnames = os.listdir(input_dir)
    meeting_list: List[Meeting] = []
    for n, output_fname in enumerate(output_fnames):
        with open(f"{input_dir}/{output_fname}", "r") as f_in:
            html = f_in.read()
            _meeting_list = parse_playwright_output(html)
            meeting_list += _meeting_list
    
    unique_meeting_list = get_unique_meetings(meeting_list)
    flat_data_df = assemble_dataframe_and_save(unique_meeting_list)
    flat_data_df.to_json(output_fpath, orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="input playwright dir")
    parser.add_argument("--output_fpath", help="output all_data_flat.json fpath")
    args = parser.parse_args()
    if not args.input_dir or not args.output_fpath:
        raise Exception("All arguments are required")
    main(input_dir=args.input_dir, output_fpath=args.output_fpath)
