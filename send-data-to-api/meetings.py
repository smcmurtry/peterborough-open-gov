import requests
import json
import os
from dotenv import dotenv_values 

config = dotenv_values()

def send_meeting_data_to_api():
    responses = []
    headers = {"content-type": "application/json"}
    datafile = "python-etl-scraper/generated_data/all_data_flat.json"
    
    with open(datafile, "r") as file:
        data = json.load(file)
        for meeting in data:
            date = meeting["datetime_iso"].split("T")[0]
            fname_part = meeting["meeting_type"].replace(" ", "-")
            data = {
                "id": meeting["id"],
                "name": meeting["meeting_type"],
                "location": meeting["location"],
                "date": meeting["datetime_iso"],
                "minutes_fname": f"{date}.{fname_part}.pdf", 
            }
            response = requests.post(f"{config['API_URL']}/meetings", json=data, headers=headers)
            responses.append(response)
    return responses

responses = send_meeting_data_to_api()
print("responses", responses)