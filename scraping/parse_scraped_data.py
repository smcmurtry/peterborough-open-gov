import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import json

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


def main(
        input_fpath: str = "../playwright_output/output.txt",
        output_fpath: str = "generated_data/playwright_data.json"
    ):
    """
    This takes the scraped playwright data as input and writes the meeting
    data to file. The meeting data is of type: List[Meeting]
    """
    with open(input_fpath, "r") as f_in:
        html = f_in.read()
        meeting_list = parse_playwright_output(html)
        with open(output_fpath, "w") as f_out:
            json.dump(meeting_list, f_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input playwright file fpath")
    parser.add_argument("--output", help="output data file fpath")
    args = parser.parse_args()
    if not args.input or not args.output:
        raise Exception("Both input and output are required")
    main(input_fpath=args.input, output_fpath=args.output)
