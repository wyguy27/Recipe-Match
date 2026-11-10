"""
(EVENTUALLY) Fills the local SQLite database with information from 99 (daily limit) recipes from a cuisine.
Ensure you have a ".env" file with an API_KEY variable in your project's root directory.
"""

import os, json, requests
from dotenv import load_dotenv


TEST_API_URL = r"https://api.spoonacular.com/recipes/complexSearch"
load_dotenv(".env") # Loads .env vars
API_KEY = os.getenv("API_KEY")
PARAMS = {
    "apiKey": API_KEY,
    "addRecipeInformation": "true",
    "addRecipeInstructions": "true",
    "instructionsRequired": "true",
    "number": "1",
}

if __name__ == "__main__":
    res = call()
    print(f"{res.status_code=}\n{res.text=}")

def search_Recipes() -> requests.Response:
    return requests.get("https://api.spoonacular.com/recipes/complexSearch", params=PARAMS)
