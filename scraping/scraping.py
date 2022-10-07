import requests
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


def run():
    meetings_page = requests.get(meetings_url)
    soup = BeautifulSoup(meetings_page.text, "html.parser")
    meeting_type_anchors = soup.find_all("a", {"class": "PastMeetingTypesName"})
    meeting_type_hrefs = [x.attrs["href"] for x in meeting_type_anchors]

    parsed_meetings: List[Meeting] = []
    for n, href in enumerate(meeting_type_hrefs[10:]):
        n = n + 10
        print(f"{n} of {len(meeting_type_hrefs)}")
        meeting_type_page = requests.post(href)
        parsed_meetings_of_type = parse_meeting_page_text(meeting_type_page.text)
        parsed_meetings += parsed_meetings_of_type
        with open(f"data/part_{n}.json", "w") as f:
            json.dump(parsed_meetings_of_type, f)
