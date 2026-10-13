from django.urls import path

from . import views

urlpatterns = [
    path("", views.base, name="base"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("search/", views.search, name="search"),
    path("inherit/", views.inherit, name="inherit")
]