from typing import List, TypedDict


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


class MeetingFlat(TypedDict):
    id: str
    meeting_type: str
    location: str
    datetime_iso: str
    agenda_url: str
    minutes_html_url: str
    minutes_pdf_url: str
    cancelled: bool
    video_url: str


class MinutesData(TypedDict):
    pdf_fname: str
    html_fname: str
    url: str
