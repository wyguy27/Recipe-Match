import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    return render(request, "recipes/homepage.html")

def recipe(request, recipe_id):
    response = "You are looking at %s."
    return HttpResponse(response % recipe_id)

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
        'apiKey': settings.SPOONACULAR_API_KEY,
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
    return HttpResponse("You are at the about page.")
