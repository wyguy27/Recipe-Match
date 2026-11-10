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

    if not query:
        return render(request, 'recipes/results.html', {
            'results': [],
            'query': ''
        })

    url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        'apiKey': settings.SPOONACULAR_API_KEY,
        'query': query,
        'number': 10
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get('results', [])

        #print(response.text)

        return render(request, 'recipes/results.html', {
            'results': results,
            'query': query
        })

    except requests.RequestException:
        return render(request, 'recipes/results.html', {
            'results': [],
            'query': query,
            'error': 'Unable to retrieve recipes. Please try again.'
        })

def about(request):
    return HttpResponse("You are at the about page.")
