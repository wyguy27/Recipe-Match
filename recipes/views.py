from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "recipes/index.html")


def recipe(request, recipe_id):
    response = "You are looking at %s."
    return HttpResponse(response % recipe_id)

def search(request):
    return HttpResponse("You are at the search page.")
