from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Hello, world. You're at the recipes index.")
    render(request, "templates/recipes/index.html")
def recipe(request):
    return HttpResponse("You are at the Recipe page. ")

def search(request):
    return HttpResponse("You are at the search page.")


