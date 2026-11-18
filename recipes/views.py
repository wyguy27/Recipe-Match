from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.templatetags.static import static
from dataclasses import dataclass
from models import Recipe, Ingredient, RecipeIngredient, Cuisine, Diet, Equipment, RecipeType, Intolerance
import random, requests

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

def recipe(request, recipe_id):
    response = "You are looking at %s."
    return HttpResponse(response % recipe_id)

def search(request):
    query = request.GET.get('search', '').strip()
    cuisine = request.GET.get('cuisine', '').strip()
    calorie = request.GET.get('calorie', '').strip()

    diets = []

    if request.GET.get('gluten'):
        diets.append('gluten free')
    if request.GET.get('keto'):
        diets.append('ketogenic')
    if request.GET.get('vegetarian'):
        diets.append('vegetarian')
    if request.GET.get('vegan'):
        diets.append('vegan')
    if request.GET.get('pescetarian'):
        diets.append('pescetarian')
    diet = ','.join(diets)

    if not query:
        return render(request, 'recipes/results.html', {
            'results': [],
            'query': '',
            'cuisine': cuisine,
            'diet': diet,
            'maxCalories': calorie
        })

    url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        'query': query,
        'cuisine': cuisine,
        'diet': diet,
        'maxCalories': calorie if calorie else 1000000,
        'number': 10
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get('results', [])

        print(f"RESULTS: {response.text}")

        return render(request, 'recipes/results.html', {
            'results': results,
            'query': query,
            'cuisine': cuisine,
            'diet': diet,
            'maxCalories': calorie
        })

    except requests.RequestException:
        return render(request, 'recipes/results.html', {
            'results': [],
            'query': query,
            'cuisine': cuisine,
            'diet': diet,
            'maxCalories': calorie,
            'error': 'Error. Please try again.'
        })

def about(request):
    return HttpResponse("You are at the about page.")