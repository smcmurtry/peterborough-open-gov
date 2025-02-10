import requests
import json
import os
from dotenv import dotenv_values 

config = dotenv_values()

def send_vote_data_to_api():
    responses = []
    headers = {"content-type": "application/json"}
    votes_dir = "python-etl-scraper/votes/"
    
    for filename in os.listdir(votes_dir):
        if not filename.endswith('.json'):
            continue
            
        with open(f"{votes_dir}{filename}", "r") as file:
            vote_data = json.load(file)
            # query for the meeting_id using filename
            date = filename.split(".")[0]
            meeting_name = filename.split(".")[1].replace("-", " ")
            
            try:
                response = requests.get(f"{config['API_URL']}/meetings/search", 
                                    params={"name": meeting_name, "date": date})
                meeting_id = response.json()[0]["id"]

                for vote in vote_data:
                    data = {
                        "meeting_id": meeting_id,
                        "title": vote["title"],
                    }
                    response = requests.post(f"{config['API_URL']}/votes", json=data, headers=headers)
                    vote_id = response.json()["id"]

                    for councillor in vote["for"]:
                        councillor_id = councillor.replace(" ", "_").lower()
                        data = {
                            "councillor_id": councillor_id,
                            "vote_id": vote_id,
                            "title": vote["title"],
                            "vote": "for",
                        }
                        response = requests.post(f"{config['API_URL']}/councillor_votes", json=data, headers=headers)
                        responses.append(response)

                    for councillor in vote["against"]:
                        data = {
                            "councillor_id": councillor_id,
                            "vote_id": vote_id,
                            "title": vote["title"],
                            "vote": "against",
                        }
                        response = requests.post(f"{config['API_URL']}/councillor_votes", json=data, headers=headers)
                        responses.append(response)
            except:
                print("Error getting meeting_id for", meeting_name, date)
    return responses

responses = send_vote_data_to_api()
print("responses", responses)