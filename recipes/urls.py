from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("cuisine/<int:cuisine_id>/", views.cuisine, name="cuisine"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
]