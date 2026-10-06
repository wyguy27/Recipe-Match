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

# This method calls for a recipes entire stored information from Spoonacular
# Inputs: TEST_API_URL: The stored value for the base URl
#         params: The stored additions to the URL(Set to the PARAM container)
# Outputs: A recipes entire raw information to be parsed within parse_recipe
# Author: Derrick
def call() -> requests.Response:
    """(TODO: Allow customizable queries) Queries Spoonacular API for recipe information"""
    return requests.get(TEST_API_URL, params=PARAMS)

#This method parses the raw information and stores it into a separate file in JSON format
def parse_recipe():
    api_data = requests.get(TEST_API_URL, params=PARAMS)
    with open("Recipes.JSON", "w", encoding= "utf-8") as write_file:
        json.dump(api_data.json(),write_file)
    pass

#This method will help to break down the recipe further to understand the categories the ingredients fall into
def parse_ingredient():
    """Parses desired ingredient information to be saved to the local database"""
    pass


if __name__ == "__main__":
    res = parse_recipe()