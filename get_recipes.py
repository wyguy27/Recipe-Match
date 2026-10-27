"""
Fills the local SQLite database with information from 700 recipes (daily limit).
Ensure you have a ".env" file with an API_KEY variable in your project's root directory.
"""

import os, json, requests
#from recipes.models import Recipe, Ingredient, RecipeIngredient
from dotenv import load_dotenv

load_dotenv(".env")

API_URL = r"https://api.spoonacular.com/recipes/complexSearch"
API_KEY = os.getenv("API_KEY")
DEFAULT_IMAGE_URL = r"https://assets.streamlinehq.com/image/private/w_512,h_512,ar_1/f_auto/v1/icons/3/pot-of-food-izlc75pz5zn1vq7wmss271.png/pot-of-food-0hiupzos5jj250o6ivxo4.png?_a=DATAiZAAZAA0"
BASE_PARAMS = {
    "apiKey": API_KEY,
    "addRecipeInformation": "true",
    "addRecipeInstructions": "true",
    "instructionsRequired": "true",
    "number": '1',
    "offset": '0',
}


# This helper method calls for a recipes entire stored information from Spoonacular
# Inputs: API_URL: The stored value for the base URl
#         params: The stored additions to the URL(Set to the PARAM container)
# Outputs: A recipes entire raw information to be parsed within parse_recipe
# Author: Derrick
def call(api_url:str=API_URL, params:dict=BASE_PARAMS) -> requests.Response:
    """Queries Spoonacular API for recipe information"""
    api_data:requests.Response = requests.get(api_url, params=params, timeout=20)
    api_data.raise_for_status()
    return api_data


# This method parses the raw information and stores it into a separate file in JSON format.
# Author: Derrick
def parse_call(api_data: requests.Response) -> dict:
    """
    Parses response JSON to extract useful information
    about recipes and ingredients.
    """
    data: dict = api_data.json()
    results: dict = data.get("results", {})[0] # TODO: CHECK IF THIS IS CONSISTENT, for some reason they store "results" as a dict in a list
    parsed: dict = {}

    # Fetches all needed data. Figures out the necessary formats and mappings to models.
    spoonacular_id: str | None = results.get("id", None)
    if spoonacular_id is None:
        return {}
    parsed["spoonacular_id"] = spoonacular_id
    parsed["image"] = results.get("image", DEFAULT_IMAGE_URL)
    parsed["name"] = results.get("title", "Recipe")
    parsed["ready_time"] = results.get("readyInMinutes", "Unknown")
    parsed["servings"] = results.get("servings", "Unknown")
    parsed["cuisines"] = results.get("cuisines", [])
    parsed["types"] = results.get("dishTypes", [])
    parsed["diets"] = results.get("diets", [])
    parsed["intolerances"] = results.get("intolerances", [])
    # TODO (The following are formatted strange or appear in multiple places)
    parsed["equipment"] = [] #TODO
    parsed["instructions"] = "" #TODO

    for key, val in parsed.items():
        print(f"{key}: {val}")

    return parsed

def parse_equipment(api_data: requests.Response) -> dict:
    """
    Parses response JSON to extract useful information
    about equipment
    """
    data: dict = api_data.json()
    results: dict = data.get("results", {})[0] # TODO: CHECK IF THIS IS CONSISTENT, for some reason they store "results" as a dict in a list
    parsed: dict = {}

def parse_ingredients(api_data: requests.Response) -> dict:
    """
    Parses response JSON to extract useful information
    about ingredient amount
    """
    data: dict = api_data.json()
    results: dict = data.get("results", {})[0] # TODO: CHECK IF THIS IS CONSISTENT, for some reason they store "results" as a dict in a list
    parsed: dict = {}

# Author: Julian
def store_call(api_data: requests.Response, filename:str="recipe") -> None:
    """Stores an API response to a local JSON file"""
    with open(f"{filename}.json", 'w', encoding= "utf-8") as file:
        json.dump(api_data.json(), file)


def populate_recipe(number:str='1', offset:str='0') -> None:
    """Stores recipe information into Django's SQLite DB"""
    params = BASE_PARAMS # This is probably terrible design, sorry
    params["number"] = number
    params["offset"] = offset
    api_data: requests.Response = call(params=params)
    store_call(api_data) # Stores original response to "recipe.json"
    parse_call(api_data)

def populate_equipment():
    API_URL = r"https://api.spoonacular.com/recipes/1003464/equipmentWidget.json"

    parse_equipment()

def populate_ingred_amount():
    API_URL = r"https://api.spoonacular.com/recipes/1003464/ingredientWidget.json"

    parse_ingredients()


if __name__ == "__main__":
    populate_recipe()
    populate_equipment()