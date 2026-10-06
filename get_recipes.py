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


def call() -> requests.Response:
    """(This is bad, clean this up) Queries Spoonacular API for recipe information"""
    return requests.get(TEST_API_URL, params=PARAMS)


if __name__ == "__main__":
    res = call()
    print(f"{res.status_code=}\n{res.text=}")