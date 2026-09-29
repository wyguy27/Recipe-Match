from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the recipe index.")

def search(request):
    return HttpResponse("Hello, world. You're at the recipe search.")

def history(request):
    return HttpResponse("Hello, world. You're at your recipe history.")