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

def example(request):
    template = loader.get_template("base.html")
    return HttpResponse(template.render({}, request))

def temp(request):
    template = loader.get_template("recipes/test.html")
    return HttpResponse(template.render({}, request))