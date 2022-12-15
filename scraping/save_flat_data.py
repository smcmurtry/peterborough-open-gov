import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict
from my_types import MinutesData


from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib import parse

import scraping


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
    df[cols_of_interest].to_json("generated_data/all_data_flat.json", orient="records")

    all_meeting_types = list(set(df["meeting_type"]))
    with open("generated_data/all_meeting_types.json", "w") as f:
        json.dump(all_meeting_types, f)


def main():
    with open("../playwright_output/output.txt", "r") as f:
        html = f.read()
        all_data = scraping.parse_playwright_output(html)
    assemble_dataframe_and_save(all_data)

if __name__ == "__main__":
    main()
