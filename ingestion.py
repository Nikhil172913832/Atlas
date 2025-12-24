import requests
import yaml
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

with open("conf.yaml") as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)
load_dotenv()

YOUTUBE_DATA_API_URL = config["youtube_data_api_url"]
API_KEY = os.getenv("API_KEY")

base_params = {
    "part": "snippet",
    "key": API_KEY,
    "maxResults": 4,
    "relevanceLanguage": "en",
}

app = FastAPI()

@app.get("/fetch_results_youtube/")
def fetch_results_youtube(query: str, pageToken: str | None = None):
    try:
        params = base_params.copy()
        params["q"] = query
        if pageToken:
            params["pageToken"] = pageToken
        result = requests.get(YOUTUBE_DATA_API_URL, params=params)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Upstream API error: {e.response.status_code}"
        )
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Upstream service unreachable")
