import requests, os
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.db.models import F
from dotenv import load_dotenv
from .models import Recipe, Cuisine, Ingredient, RecipeIngredient

load_dotenv()
SPOONACULAR_API_KEY = os.getenv("API_KEY")
POPULAR_RECIPE_COUNT = 9
POPULAR_CUISINE_COUNT = 6
CUISINE_RECIPE_COUNT = 9


def clean_recipe_images(recipes):
    cleaned_recipes = recipes
    for recipe in cleaned_recipes:
        if not recipe.image:
            recipe.image = "" # static(r"recipes/food.png")

    return cleaned_recipes


def index(request):
    popular_recipes = Recipe.objects.order_by('-visited_count')[:POPULAR_RECIPE_COUNT]
    popular_recipes = clean_recipe_images(popular_recipes)

    popular_cuisines = [{"id": cuisine.pk, "cuisine": cuisine.name}
        for cuisine in Cuisine.objects.all()
    ]

    return render(request, "recipes/homepage.html", {
        "popular_foods" : popular_recipes,
        "popular_cuisines" : popular_cuisines,
    })


def cuisine(request, cuisine_id):
    cuisine = get_object_or_404(Cuisine, pk=cuisine_id)

    recipes = Recipe.objects.filter(cuisines=cuisine_id).order_by("-visited_count")[:CUISINE_RECIPE_COUNT]
    for recipe in recipes:
        print(recipe)
    return render(request, "recipes/cuisine.html", {
        "cuisine" : cuisine.name,
        "recipes" : recipes,
    })


def recipe(request, recipe_id):
    recipe_obj = get_object_or_404(Recipe, pk=recipe_id)
    Recipe.objects.filter(pk=recipe_obj.pk).update(visited_count=F("visited_count") + 1)
    ingredients = Ingredient.objects.filter(recipe_ingredients__recipe=recipe)

    return render(request, "recipes/recipe.html", {
        "recipe": recipe_obj,
        "recipe_ingredients": ingredients,
    })


def search(request):
    return render(request, 'recipes/search.html')


def results(request):
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
        'apiKey': SPOONACULAR_API_KEY,
        'query': query,
        'cuisine': cuisine,
        'diet': diet,
        'maxCalories': calorie if calorie else 1000000,
        'number': 10
    }
    # print(params)

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
    return HttpResponse("You are at the about us page.")