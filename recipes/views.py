from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Cuisine, Recipe

POPULAR_RECIPE_COUNT = 9
POPULAR_CUISINE_COUNT = 4
CUISINE_RECIPE_COUNT = 9

def popular_recipes(queryset=None):
    """Recipes ordered by visits, with id as a stable tie-breaker."""
    if queryset is None:
        queryset = Recipe.objects.all()
    return queryset.order_by("-visited_count", "id")


def index(request):
    popular_foods = popular_recipes()[ : POPULAR_RECIPE_COUNT]
    popular_cuisines = (
        Cuisine.objects
        .annotate(total_visits=Sum("recipes__visited_count"), recipe_count=Count("recipes"))
        .filter(recipe_count__gt=0)
        .order_by("-total_visits", "-recipe_count", "name")[ : POPULAR_CUISINE_COUNT]
    )
    return render(request, "recipes/homepage.html", {
        "popular_foods" : popular_foods,
        "popular_cuisines" : popular_cuisines,
    })

def cuisine(request, cuisine_id):
    cuisine = get_object_or_404(Cuisine, pk=cuisine_id)
    recipes = popular_recipes(cuisine.recipes.all())[ : CUISINE_RECIPE_COUNT]
    return render(request, "recipes/cuisine.html", {
        "cuisine" : cuisine.name,
        "recipes" : recipes,
    })

def recipe(request, recipe_id):
    response = "You are looking at %s."
    return HttpResponse(response % recipe_id)

def search(request):
    return HttpResponse("You are at the search page.")

def about(request):
    return HttpResponse("You are at the about page.")
