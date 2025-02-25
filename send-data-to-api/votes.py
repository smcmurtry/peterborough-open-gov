import requests
import json
import os
from dotenv import dotenv_values 
import uuid

config = dotenv_values()

def send_vote_data_to_api():
    responses = []
    headers = {"content-type": "application/json"}
    datafile = "python-etl-scraper/generated_data/all_vote_data.json"

    with open(datafile, "r") as file:
        vote_data = json.load(file)
        # todo: change the key to the meeting_id
        # query for the meeting_id using filename
        for meeting_filename in vote_data.keys():
            date = meeting_filename.split(".")[0]
            meeting_name = meeting_filename.split(".")[1].replace("-", " ")
            
            try:
                response = requests.get(f"{config['API_URL']}/meetings/search", 
                                    params={"name": meeting_name, "date": date})
                if response.status_code != 200:
                    continue
                meeting_id = response.json()[0]["id"]
                _vote_data = vote_data[meeting_filename]
                for vote in _vote_data:
                    vote_id = str(uuid.uuid4())
                    data = {
                        "id": vote_id,
                        "meeting_id": meeting_id,
                        "title": vote["title"][:254], # truncate the title to fit in the db
                        "carried": vote["carried"],
                    }
                    response = requests.post(f"{config['API_URL']}/votes", json=data, headers=headers)
                    if response.status_code != 201:
                        print(response.content)
                        continue

                    for councillor in vote["for"]:
                        councillor_id = councillor.split(" ")[1].lower()
                        data = {
                            "councillor_id": councillor_id,
                            "vote_id": vote_id,
                            "vote_cast": "for",
                        }
                        response = requests.post(f"{config['API_URL']}/councillor_votes", json=data, headers=headers)
                        if response.status_code != 201:
                            print(response.content)
                        responses.append(response)

                    for councillor in vote["against"]:
                        councillor_id = councillor.split(" ")[1].lower()
                        data = {
                            "councillor_id": councillor_id,
                            "vote_id": vote_id,
                            "vote_cast": "against",
                        }
                        response = requests.post(f"{config['API_URL']}/councillor_votes", json=data, headers=headers)
                        if response.status_code != 201:
                            print(response.content)

                        responses.append(response)
            except Exception as e:
                print(e)
                print("Error getting meeting_id for", meeting_name, date)
    return responses

responses = send_vote_data_to_api()
print("responses", responses)