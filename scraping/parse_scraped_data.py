import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.parse import parse_qs
from urllib import parse

from typing import List, TypedDict

url = "https://www.peterborough.ca/en/city-hall/upcoming-and-past-agendas.aspx"

# meetings_url = "https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent&Year=2021"
meetings_url = "https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent"
post_url_2 = "https://pub-peterborough.escribemeetings.com/MeetingsCalendarView.aspx/PastMeetings?FillWidth=1&wmode=transparent&Year=2021&Expanded=Airport%20Strategic%20Initiatives%20Committee"

# So I need to find the links like `post_url_2` above in the `meetings_page`. And then do a post request and that should
# give me the list of urls for the minutes, agendas, videos, etc.


def parse_meeting_date(datetime_str: str) -> str:
    "datetime_str like Monday, 'December 06, 2021 @  6:30 PM'"
    string_format = "%A, %B %d, %Y @ %I:%M %p"
    parsed = datetime.strptime(datetime_str, string_format)
    return parsed.isoformat()


class Link(TypedDict):
    aria_label: str
    link_text: str
    href: str
    url: str


class Meeting(TypedDict):
    datetime_iso: str
    meeting_type: str
    location: str
    links: List[Link]


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


def parse_meeting_page_text(meeting_page_text) -> List[Meeting]:
    soup = BeautifulSoup(meeting_page_text, "html.parser")
    past_meeting_soup = soup.find("div", {"class": "past-meetings"})
    if not past_meeting_soup:
        return []
    all_meetings_of_type_2021 = past_meeting_soup.find_all(
        "div", {"class": "meeting-header"}
    )
    parsed_meetings = []
    for meeting_soup in all_meetings_of_type_2021:
        meeting = parse_meeting_soup(meeting_soup)
        parsed_meetings.append(meeting)
    return parsed_meetings


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


def main(
        input_fpath = "../playwright_output/output.txt",
        output_fpath = "generated_data/all_data_flat.json"
    ):
    """
    This takes the scraped playwright data as input and writes the meeting
    data to file. The meeting data is of type: List[Meeting]
    """
    with open(input_fpath, "r") as f_in:
        html = f_in.read()
        meeting_list = parse_playwright_output(html)

        flat_data_df = assemble_dataframe_and_save(meeting_list)
        flat_data_df.to_json(output_fpath, orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input playwright file fpath")
    parser.add_argument("--output", help="output all_data_flat.json fpath")
    args = parser.parse_args()
    if not args.input or not args.output:
        raise Exception("Both input and output are required")
    main(input_fpath=args.input, output_fpath=args.output)
