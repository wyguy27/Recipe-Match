from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    template = loader.get_template("recipes/index.html")
    return HttpResponse(template.render({}, request))

def recipe(request):
    return HttpResponse("Hello, wgvhjkuikgjcfguhkyjchfgjjvc")

def search(request):
    template = loader.get_template("recipes/search.html")
    return HttpResponse(template.render({}, request))