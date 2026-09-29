"""
(EVENTUALLY) Fills the local SQLite database with information from 99 (daily limit) recipes from a cuisine.
Ensure you have a ".env" file with an API_KEY variable in your project's root directory.
"""

import os, json, requests
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from recipes.models import (
    Recipe, Ingredient, RecipeIngredient, Cuisine,
    Diet, Intolerance, Equipment, RecipeType
)

BASE_API_URL = r"https://api.spoonacular.com"
load_dotenv(".env") # Loads .env vars
API_KEY = os.getenv("API_KEY")


def call(query: str) -> None:
    """Queries Spoonacular API for recipe information"""
    pass



def main() -> None:
    query: str = f""


if __name__ == "__main__":
    main()