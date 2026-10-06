"""
(EVENTUALLY) Fills the local SQLite database with information from 700 recipes (daily limit).
Ensure you have a ".env" file with an API_KEY variable in your project's root directory.
"""

import os, json, requests
from dotenv import load_dotenv


TEST_API_URL = r"https://api.spoonacular.com/recipes/complexSearch"
load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
PARAMS = {
    "apiKey": API_KEY,
    "addRecipeInformation": "true",
    "addRecipeInstructions": "true",
    "instructionsRequired": "true",
    "number": "1",
}


def call() -> dict:
    """(TODO: Allow customizable queries) Queries Spoonacular API for recipe information"""
    res: requests.Response = requests.get(TEST_API_URL, params=PARAMS)
    return res.json()


def parse_response(res: dict) -> dict[str, str | list]:
    """Parses a recipe response and saves as a JSON fixture"""
    


if __name__ == "__main__":
    res: dict = call()
    