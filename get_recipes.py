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


def call() -> requests.Response:
    """(TODO: Allow customizable queries) Queries Spoonacular API for recipe information"""
    return requests.get(TEST_API_URL, params=PARAMS)


def parse_recipe():
    """Parses desired recipe information to be saved to the local database"""
    
    pass


def parse_ingredient():
    """Parses desired ingredient information to be saved to the local database"""
    pass


if __name__ == "__main__":
    res = call()
    print(f"{res.status_code=}\n{res.text=}")