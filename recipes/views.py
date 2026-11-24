from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.templatetags.static import static
import requests
from .models import Recipe, Cuisine, Ingredient, RecipeIngredient


def clean_recipe_images(recipes):
    cleaned_recipes = recipes
    for recipe in cleaned_recipes:
        if not recipe.image:
            recipe.image = "" # static(r"recipes/food.png")

    return cleaned_recipes


def index(request):
    popular_recipes = Recipe.objects.order_by('-visited_count')[:6]
    popular_recipes = clean_recipe_images(popular_recipes)

    popular_cuisines = Cuisine.objects.all()

    return render(request, "recipes/homepage.html", {
        "popular_foods" : popular_recipes,
        "popular_cuisines" : popular_cuisines,
    })


def cuisine(request, cuisine_id):
    try:
        cuisine = Cuisine.objects.get(id=cuisine_id)
    except (Cuisine.DoesNotExist):
        raise Http404("Cuisine does not exist")

    recipes = Recipe.objects.filter(cuisine=cuisine).order_by("-visited_count")[:6]
    return render(request, "recipes/cuisine.html", {
        "cuisine" : cuisine_id,
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