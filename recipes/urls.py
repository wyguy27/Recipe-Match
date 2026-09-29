from django.urls import path

from . import views

urlpatterns = [
    # ex: /recipes/
    path("", views.index, name="index"),
    # ex: /recipes/search/
    path("search/", views.search, name="search"),
    # ex: /recipes/history/
    path("history/", views.history, name="history"),
]