from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("search/", views.search, name="search"),
    path("base/", views.base, name="base"),
    path("inherit/", views.inherit, name="inherit")
]