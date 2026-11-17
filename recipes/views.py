from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Hello, world. You're at the recipes index.")
    return render(request, "recipes/index.html")
def recipe(request, recipe_id):
    return render(request, "recipes/recipe.html", {"recipe_id": recipe_id})

def search(request):
    return HttpResponse("You are at the search page.")
def about(request):
    return HttpResponse("About page (placeholder).")

