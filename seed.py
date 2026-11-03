"""
Populates DB with recipe, ingredient, and related information.
Ensure you have a ".env" file with an API_KEY variable in your project's root directory.
"""

import os, sys, json, requests, django
from dotenv import load_dotenv

DJANGO_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"recipes")
sys.path.insert(0, DJANGO_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from recipes.models import Recipe, Ingredient, RecipeIngredient, Cuisine, Diet, Equipment, RecipeType, Intolerance

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


def parse_call(api_data: requests.Response):
    """
    Parses response JSON to extract useful information
    about recipes, ingredients, and related info.
    This is then stored into Django's SQLite3 DB.
    """
    data: dict = api_data.json()

    for recipe_data in data.get("results", []):
        instructions = []
        seen_equipment = set()
        equipment_instances = []
        seen_ingredients = set()
        ingredient_instances = []
        analyzed_instructions = recipe_data.get("analyzedInstructions", [])

        for instruction in analyzed_instructions:
            steps = instruction.get("steps", []).strip()

            for step in steps:
                num = step.get("number", "")
                text = step.get("step", "").strip()
                if text:
                    instructions.append(f"Step {num}: {text}")

                for equipment in step.get("equipment", []):
                    equipment_id = equipment.get("id")
                    if equipment_id and equipment_id not in seen_equipment:
                        seen_equipment.add(equipment_id)
                        eq, _ = Equipment.objects.update_or_create(
                            spoonacular_id=equipment_id,
                            defaults={
                                "name": equipment.get("name", "Unknown"),
                                "image": equipment.get("image", ""),
                            }
                        )
                        equipment_instances.append(eq)

                for ingredient in step.get("ingredients", []):
                    ingredient_id = ingredient.get("id")

                    if ingredient_id and ingredient_id not in seen_ingredients:
                        seen_ingredients.add(ingredient_id)
                        ing, _ = Ingredient.objects.update_or_create(
                            spoonacular_id=ingredient_id,
                            defaults={
                                "name": ingredient.get("name") or ingredient.get("localizedName", ""),
                            }
                        )
                        ingredient_instances.append(ing)

        instructions_formatted = "\n\n".join(instructions) if instructions else ""
        recipe, _ = Recipe.objects.update_or_create(
            spoonacular_id = recipe_data.get("id"),
            defaults={
                "name": recipe_data.get("title", "Unknown Recipe"),
                "image": recipe_data.get("image", ""),
                "ready_time": recipe_data.get("readyInMinutes"),
                "servings": recipe_data.get("servings"),
                "instructions": instructions_formatted,
                "source_url": recipe_data.get("spoonacularSourceUrl", "https://spoonacular.com/"),
            }
        )

        diets = [Diet.objects.update_or_create(name=diet)[0] for diet in recipe_data.get("diets", [])]
        cuisines = [Cuisine.objects.update_or_create(name=cuisine)[0] for cuisine in recipe_data.get("cuisines", [])]
        recipe_types = [RecipeType.objects.update_or_create(name=recipe_type) for recipe_type in recipe_data.get("dishTypes", [])]
        #intolerances = [Intolerance.objects.update_or_create(name=intolerance) for intolerance in recipe_data.get("intolerances", [])]

        # Adds many-to-many relationships to Recipe
        recipe.diets.set(diets)
        recipe.cuisines.set(cuisines)
        recipe.types.set(recipe_types)
        #recipe.intolerances.set(intolerances)
        recipe.equipment.set(equipment_instances)

        # Adds all RecipeIngredients associated with this recipe
        for ing in ingredient_instances:
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ing,
            )


"""
# This method parses the raw information and stores it into a separate file in JSON format.
# Author: Derrick
def parse_call(api_data: requests.Response) -> dict:
    """"""
    Parses response JSON to extract useful information
    about recipes and ingredients.
    """"""
    data: dict = api_data.json()
    results: dict = data.get("results", [{}])[0]
    instructions: list = results.get("analyzedInstructions", [{}])[0].get("steps", [])
    parsed: dict = {}
    store_call(instructions, "instructions")

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
    parsed["equipment"] = parse_equipment(instructions)
    parsed["instructions"] = parse_instructions(instructions)

    for key, val in parsed.items():
        print(f"{key}: {val}")

    return parsed


def parse_instructions(instructions: list) -> dict:
    """"""
    parsed: dict = {}
    parsed["instructions"] = ""
    parsed["ingredients"] = []
    parsed["equipment"] = []
    for instruction in instructions:
        number: int = instruction.get("number", 0)
        step_instruction: str = instruction.get("step", "")
        step_ingredients: dict = instruction.get("ingredients", [])
        step_equipment: dict = instruction.get("equipment", [])
        parsed["instructions"] += f"Step {number}:\n{step_instruction}\n\n"
        parsed["ingredients"].append(ingredient for ingredient in step_ingredients)

    return parsed
"""


# Author: Julian
def store_call(api_data: requests.Response | dict | list, filename:str="recipe") -> None:
    """Stores an API response to a local JSON file"""
    with open(f"{filename}.json", 'w', encoding= "utf-8") as file:
        data = api_data
        if isinstance(data, requests.Response):
            data = data.json()
        try:
            json.dump(data, file)
        except Exception:
            file.write("Error saving data. Check the data format.")


def populate_recipe(number:str='1', offset:str='0') -> None:
    """Stores recipe information into Django's SQLite DB"""
    params = BASE_PARAMS
    params["number"] = number
    params["offset"] = offset
    api_data: requests.Response = call(params=params)
    store_call(api_data) # Stores original response to "recipe.json"
    parse_call(api_data)

def populate_equipment():
    API_URL = r"https://api.spoonacular.com/recipes/1003464/equipmentWidget.json"

def populate_ingred_amount():
    API_URL = r"https://api.spoonacular.com/recipes/1003464/ingredientWidget.json"


if __name__ == "__main__":
    populate_recipe()
    populate_equipment()