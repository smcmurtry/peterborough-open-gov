from dotenv import load_dotenv

from flask import Flask, redirect, render_template, url_for
import json
from scraping.scraping import Meeting
from typing import List, Dict
from datetime import datetime

load_dotenv()

meeting_data: List[Meeting] = []
with open("scraping/all_data_flat.json", "r") as f:
    meeting_data = json.load(f)

def format_datetime(datetime_iso: str) -> str:
    output_format = "%B %-d, %Y, %-I:%M %p"
    dt = datetime.fromisoformat(datetime_iso)
    return datetime.strftime(dt, output_format)

try:
    for meeting in meeting_data:
        meeting["datetime_display"] = format_datetime(meeting["datetime_iso"])
except:
    print("error parsing and formating meeting iso datetimes")

all_meeting_types: List[str] = []
with open("scraping/data/all_meeting_types.json", "r") as f:
    all_meeting_types = json.load(f)

meeting_data_dict: Dict[str, List] = {}
for meeting_type in all_meeting_types:
    meeting_data_dict[meeting_type] = [x for x in meeting_data if x["meeting_type"] == meeting_type]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def home():
        variables = {"all_meeting_types": all_meeting_types}
        return render_template('home.html', **variables)

    @app.route('/meetings/<meeting_type>', methods = ['GET'])
    def meetings(meeting_type):
        if meeting_type not in meeting_data_dict:
            return render_template("404.html")
        variables = {"meeting_data": meeting_data_dict[meeting_type]}
        return render_template('meeting_list.html', **variables)


    return app