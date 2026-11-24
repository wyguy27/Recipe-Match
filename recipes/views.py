from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.db.models import F

import random
from .models import Recipe

# Placeholder data until the backend can supply real recipes and cuisines
IMAGES = ["food.png", "html_logo.png"]
CUISINES = ["Cuisine1 long long long long long long long long long long", "Cuisine2", "Cuisine3", "Cuisine4"]

def make_recipes(names):
    return [
        {"id" : i, "name" : name, "image" : static(f"recipes/{random.choice(IMAGES)}")}
        for i, name in enumerate(names, start=1)
    ]

def index(request):
    names = ["Test1 long long long long long long long long long long", "Test2", "Test3", "Test4", "Test5", "Test6", "Test7", "Test8", "Test9"]
    popular_foods = make_recipes(names)
    popular_cuisines = [
        {"id" : i, "cuisine" : cuisine}
        for i, cuisine in enumerate(CUISINES, start=1)
    ]
    return render(request, "recipes/homepage.html", {
        "popular_foods" : popular_foods,
        "popular_cuisines" : popular_cuisines,
    })

def cuisine(request, cuisine_id):
    if not 1 <= cuisine_id <= len(CUISINES):
        raise Http404("Cuisine not found")
    name = CUISINES[cuisine_id - 1]
    recipes = make_recipes([f"{name} Recipe {n}" for n in range(1, 7)])
    return render(request, "recipes/cuisine.html", {
        "cuisine" : name,
        "recipes" : recipes,
    })


#def recipe(request, recipe_id):
    #return render(request, "recipes/recipe.html", {"recipe_id": recipe_id})

def recipe(request, recipe_id):
    recipe_obj = get_object_or_404(Recipe, pk=recipe_id)
    Recipe.objects.filter(pk=recipe_obj.pk).update(visited_count=F("visited_count") + 1)

    return render(request, "recipes/recipe.html", {
        "recipe": recipe_obj,
        "recipe_ingredients": recipe_obj.ingredients.select_related("ingredient"),
    })

def search(request):
    return HttpResponse("You are at the search page.")

def about(request):
    return HttpResponse("You are at the about page.")

