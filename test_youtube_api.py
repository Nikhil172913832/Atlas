import requests
import yaml
import os
from dotenv import load_dotenv

with open("conf.yaml") as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)
load_dotenv()

YOUTUBE_DATA_API_URL=config["youtube_data_api_url"]
API_KEY=os.getenv("API_KEY")
QUERY_STRING="Machine learning"
params = {"part":"snippet", "key":API_KEY, "q":QUERY_STRING, "maxResults": 1, "relevanceLanguage": "en"}
pageToken=None
for i in range(5):
    print('-'*10)
    print(f'{i+1} Request')
    if pageToken:
        params["pageToken"] = pageToken
    result = requests.get(YOUTUBE_DATA_API_URL, params=params)
    print(result.json()['items'][0]['snippet']['title'])
    pageToken=result.json()['nextPageToken']
print('-'*10)
