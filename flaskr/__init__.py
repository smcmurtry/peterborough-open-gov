from dotenv import load_dotenv

from flask import Flask, redirect, render_template, url_for
import json
from scraping.scraping import Meeting

load_dotenv()

meeting_data: Meeting = []
with open("scraping/all_data_flat.json", "r") as f:
    meeting_data = json.load(f)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/')
    def hello():
        variables = {"meeting_data": meeting_data[:30]}
        return render_template('meeting_list.html', **variables)


    return app