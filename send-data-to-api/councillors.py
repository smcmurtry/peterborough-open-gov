import requests
import json
from dotenv import dotenv_values 

config = dotenv_values()

municipal_election_dates = [
    "2022-10-24",
    "2018-10-22",
    "2014-10-27",
    "2010-10-25",
    "2006-11-13",
]

councillors_then = [
    {"id": "diane_therrien", "name": "Diane Therrien", "title": "Mayor", "Ward": "NA", "term_start": "2018-10-22", "term_end": "2022-10-24"},
    {"id": "lesley_parnell", "name": "Lesley Parnell", "title": "Councillor", "Ward": "Otonabee", "term_start": "2010-10-25", "term_end": "NA"}, # currently in 4th term: https://www.ptbotoday.ca/2022/10/27/four-more-years-for-lesley-parnell-in-otonabee-ward/
    {"id": "kim_zippel", "name": "Kim Zippel", "title": "Councillor", "Ward": "Otonabee", "term_start": "2018-10-22", "term_end": "2022-10-24"},
    {"id": "don_vassiliadis", "name": "Don Vassiliadis", "title": "Councillor", "Ward": "Monaghan", "term_start": "2014-10-27", "term_end": "NA"}, # start date from LinkedIn
    {"id": "henry_clarke", "name": "Henry Clarke", "title": "Councillor", "Ward": "Monaghan", "term_start": "1998", "term_end": "2022-10-24"}, # start date 1998 https://kawarthanow.com/2022/05/03/henry-clarke-to-run-for-mayor-of-peterborough/
    {"id": "kemi_akapo", "name": "Kemi Akapo", "title": "Councillor", "Ward": "Town", "term_start": "2018-10-22", "term_end": "2022-10-24"},
    {"id": "dean_pappas", "name": "Dean Pappas", "title": "Councillor", "Ward": "Town", "term_start": "2006-11-13", "term_end": "2022-10-24"}, # start date from https://www.thepeterboroughexaminer.com/news/municipal-elections/after-16-years-on-peterborough-city-council-dean-pappas-goes-down-to-defeat/article_4abc6a6e-bbd1-5da9-a0dc-1655d9823baf.html
    {"id": "gary_baldwin", "name": "Gary Baldwin", "title": "Councillor", "Ward": "Ashburnham", "term_start": "2018-10-22", "term_end": "NA"}, # currently in 2nd term https://www.garybaldwin.ca/
    {"id": "keith_riel", "name": "Keith Riel", "title": "Councillor", "Ward": "Ashburnham", "term_start": "2010-10-25", "term_end": "NA"}, # https://pub-peterborough.escribemeetings.com/Meeting.aspx?Id=d99d0008-3000-40a7-9c60-e04ab55fadcc&Agenda=PostMinutes&lang=English, not elected in 2006 https://en.wikipedia.org/wiki/2006_Peterborough_municipal_election, elected in 2010 https://en.wikipedia.org/wiki/2010_Peterborough_municipal_election
    {"id": "jeff_leal", "name": "Jeff Leal", "title": "Mayor", "Ward": "NA", "term_start": "2022-10-24", "term_end": "NA"},
    {"id": "kevin_duguay", "name": "Kevin Duguay", "title": "Councillor", "Ward": "Otonabee", "term_start": "2022-10-24", "term_end": "NA"},
    {"id": "matt_crowley", "name": "Matt Crowley", "title": "Councillor", "Ward": "Monaghan", "term_start": "2022-10-24", "term_end": "NA"},
    {"id": "alex_bierk", "name": "Alex Bierk", "title": "Councillor", "Ward": "Town", "term_start": "2022-10-24", "term_end": "NA"},
    {"id": "joy_lachica", "name": "Joy Lachica", "title": "Councillor", "Ward": "Town", "term_start": "2022-10-24", "term_end": "NA"},
    {"id": "andrew_beamer", "name": "Andrew Beamer", "title": "Councillor", "Ward": "Northcrest", "term_start": "2022-10-24", "term_end": "NA"},
    {"id": "dave_haacke", "name": "Dave Haacke", "title": "Councillor", "Ward": "Northcrest", "term_start": "2022-10-24", "term_end": "NA"},
]

def send_councillor_data_to_api():
    responses = []
    headers = {"content-type": "application/json"}
    with open("python-etl-scraper/data/part_0.json", "r") as file:
        data = json.load(file)
        for meeting in data[2:]:
            # print(meeting)
            date = meeting["datetime_iso"].split("T")[0]
            fname_part = meeting["meeting_type"].replace(" ", "-")
            data = {
                "name": meeting["meeting_type"],
                "location": meeting["location"],
                "date": meeting["datetime_iso"],
                "minutes_fname": f"{date}.{fname_part}.pdf", 
            }
            response = requests.post(f"{config['API_URL']}/meetings", json=data, headers=headers)
            responses.append(response)
    return responses
responses = send_councillor_data_to_api()
print("responses", responses)