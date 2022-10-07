import json
import os
import pandas as pd

# import uuid
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict
from my_types import MinutesData


from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib import parse


def compile_data():
    contents = os.listdir("data")

    all_data = []
    for x in contents:
        if ".json" not in x:
            continue
        with open(f"data/{x}", "r") as f:
            part_data = json.load(f)
            all_data += part_data

    len(all_data)

    with open("all_data.json", "w") as f:
        json.dump(all_data, f)
    return all_data


# if minutes is in aria_label.lower() then it is the minutes
# link text gives file type
def get_minues_url(links, file_type="html"):
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


def assemble_dataframe_and_save(all_data):
    df = pd.DataFrame.from_dict(all_data)
    df["agenda_url"] = df["links"].map(lambda x: x[0]["url"])
    df["minutes_html_url"] = df["links"].map(lambda x: get_minues_url(x, "html"))
    df["minutes_pdf_url"] = df["links"].map(lambda x: get_minues_url(x, "pdf"))
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
    df[cols_of_interest].to_json("all_data_flat.json", orient="records")

    all_meeting_types = list(set(df["meeting_type"]))
    with open("data/all_meeting_types.json", "w") as f:
        json.dump(all_meeting_types, f)


def load_all_data_flat():
    with open("all_data_flat.json", "r") as f:
        all_data_flat = json.load(f)
    return all_data_flat


def get_minutes_url_from_page(agenda_text: str) -> str:
    soup = BeautifulSoup(agenda_text, "html.parser")
    attachment_divs = soup.find_all("div", attrs={"class": "AgendaItemAttachment"})
    for attachment in attachment_divs:
        if "minutes" in attachment.text.lower():
            a = attachment.find("a")
            href = a.attrs["href"]
            return "https://pub-peterborough.escribemeetings.com/" + href


def req_agenda_get_minutes_url(agenda_url: str) -> str:
    time.sleep(2)
    resp = requests.get(agenda_url)
    return get_minutes_url_from_page(resp.text)


def get_doc_id(url: str) -> str:
    parsed_url = urlparse(url)
    doc_id = parse_qs(parsed_url.query)["DocumentId"][0]
    return doc_id


def save_pdf_locally(url: str):
    resp = requests.get(url)
    doc_id = get_doc_id(url)
    with open(f"minutes/{doc_id}.pdf", "wb") as f:
        f.write(resp.content)


def main():
    all_data = compile_data()
    assemble_dataframe_and_save(all_data)
    all_data_flat = load_all_data_flat()

    with open("scraped_minutes_urls.csv", "w") as f:
        f.write("id,minues_pdf_url\n")
        for n, meeting in enumerate(all_data_flat[:]):
            print(n)
            minutes_pdf_url = req_agenda_get_minutes_url(meeting["agenda_url"])
            f.write(f"{meeting['id']},{minutes_pdf_url}\n")

    df_minutes = pd.read_csv("scraped_minutes_urls.csv")
    records = list(df_minutes.to_records(index=False))

    for n, record in enumerate(records[:]):
        print(n, end=", ")
        url = record[1]
        if not url or url == "None":
            continue
        save_pdf_locally(url)
        time.sleep(2)

    minutes_dict: Dict[str, MinutesData] = {}

    for record in records:
        meeting_id = record[0]
        url = record[1]
        if url == "None":
            continue
        doc_id = get_doc_id(url)
        pdf_fname = f"{doc_id}.pdf"
        html_fname = f"{doc_id}.html"
        minutes_data: MinutesData = {
            "pdf_fname": pdf_fname,
            "html_fname": html_fname,
            "url": url,
        }
        minutes_dict[meeting_id] = minutes_data

    json.dump(minutes_dict, open("minutes_dict.json", "w"))


if __name__ == "__main__":
    main()
