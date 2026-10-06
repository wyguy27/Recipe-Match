from django.urls import path

from . import views

urlpatterns = [
    # ex: /recipes/
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("search/", views.search, name="search"),
    path("example/", views.example, name="example"),
    path("template/", views.temp, name="temp"),
]