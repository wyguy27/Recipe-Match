from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    return render(request, "recipes/homepage.html")

def recipe(request, recipe_id):
    response = "You are looking at %s."
    return HttpResponse(response % recipe_id)

def search(request):
    return HttpResponse("You are at the search page.")

def about(request):
    return HttpResponse("You are at the about page.")
