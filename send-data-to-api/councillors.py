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

councillor_data = [
    {"id": "diane_therrien", "name": "Diane Therrien", "title": "Mayor", "start_date": "2018-10-22", "end_date": "2022-10-24"},
    {"id": "lesley_parnell", "name": "Lesley Parnell", "title": "Councillor", "ward": "Otonabee", "start_date": "2010-10-25"}, # currently in 4th term: https://www.ptbotoday.ca/2022/10/27/four-more-years-for-lesley-parnell-in-otonabee-ward/
    {"id": "kim_zippel", "name": "Kim Zippel", "title": "Councillor", "ward": "Otonabee", "start_date": "2018-10-22", "end_date": "2022-10-24"},
    {"id": "don_vassiliadis", "name": "Don Vassiliadis", "title": "Councillor", "ward": "Monaghan", "start_date": "2014-10-27"}, # start date from LinkedIn
    {"id": "henry_clarke", "name": "Henry Clarke", "title": "Councillor", "ward": "Monaghan", "start_date": "1998-10-01", "end_date": "2022-10-24"}, # start date 1998, made up oct 1 https://kawarthanow.com/2022/05/03/henry-clarke-to-run-for-mayor-of-peterborough/
    {"id": "kemi_akapo", "name": "Kemi Akapo", "title": "Councillor", "ward": "Town", "start_date": "2018-10-22", "end_date": "2022-10-24"},
    {"id": "dean_pappas", "name": "Dean Pappas", "title": "Councillor", "ward": "Town", "start_date": "2006-11-13", "end_date": "2022-10-24"}, # start date from https://www.thepeterboroughexaminer.com/news/municipal-elections/after-16-years-on-peterborough-city-council-dean-pappas-goes-down-to-defeat/article_4abc6a6e-bbd1-5da9-a0dc-1655d9823baf.html
    {"id": "gary_baldwin", "name": "Gary Baldwin", "title": "Councillor", "ward": "Ashburnham", "start_date": "2018-10-22"}, # currently in 2nd term https://www.garybaldwin.ca/
    {"id": "keith_riel", "name": "Keith Riel", "title": "Councillor", "ward": "Ashburnham", "start_date": "2010-10-25"}, # https://pub-peterborough.escribemeetings.com/Meeting.aspx?Id=d99d0008-3000-40a7-9c60-e04ab55fadcc&Agenda=PostMinutes&lang=English, not elected in 2006 https://en.wikipedia.org/wiki/2006_Peterborough_municipal_election, elected in 2010 https://en.wikipedia.org/wiki/2010_Peterborough_municipal_election
    {"id": "jeff_leal", "name": "Jeff Leal", "title": "Mayor", "start_date": "2022-10-24"},
    {"id": "kevin_duguay", "name": "Kevin Duguay", "title": "Councillor", "ward": "Otonabee", "start_date": "2022-10-24"},
    {"id": "matt_crowley", "name": "Matt Crowley", "title": "Councillor", "ward": "Monaghan", "start_date": "2022-10-24"},
    {"id": "alex_bierk", "name": "Alex Bierk", "title": "Councillor", "ward": "Town", "start_date": "2022-10-24"},
    {"id": "joy_lachica", "name": "Joy Lachica", "title": "Councillor", "ward": "Town", "start_date": "2022-10-24"},
    {"id": "andrew_beamer", "name": "Andrew Beamer", "title": "Councillor", "ward": "Northcrest", "start_date": "2022-10-24"},
    {"id": "dave_haacke", "name": "Dave Haacke", "title": "Councillor", "ward": "Northcrest", "start_date": "2022-10-24"},
]

def send_councillor_data_to_api():
    responses = []
    headers = {"content-type": "application/json"}
    for councillor in councillor_data:
        response = requests.post(f"{config['API_URL']}/councillors", json=councillor, headers=headers)
        responses.append(response)
    return responses
responses = send_councillor_data_to_api()
print("responses", responses)