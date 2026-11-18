from models import Recipe, Ingredient, RecipeIngredient, Cuisine, Diet, Equipment, RecipeType, Intolerance
from dataclasses import dataclass

@dataclass
class SearchFilter:
    cuisines: list[str] = []
    ingredients: list[str] = []
    diets: list[str] = []


def fetch_popular(filter: SearchFilter):
    """Fetches the most popular recipes overall (based on view count)"""
    return Recipe.objects.filter(filter.cuisines).filter(filter.ingredients).filter(filter.diets).order_by("-visited_count") # Fix this


def fetch_ingredients():
    """Fetches all ingredients"""
    return Ingredient.objects.all()


def fetch_recipe_w_ing(filter: SearchFilter):
    """Fetches recipes using specific ingredients"""
    result = Recipe.objects.all()
    for ing in filter.ingredients:
        result = Recipe.objects.filter(recipe_ingredients__ingredient__name=ing)

    return result