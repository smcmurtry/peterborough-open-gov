import requests
import json
from dotenv import dotenv_values 

config = dotenv_values()

def send_meeting_data_to_api():
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
responses = send_meeting_data_to_api()
print("responses", responses)