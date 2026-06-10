from django.urls import path
from . import views

urlpatterns = [
   path("", views.home, name="home"),
   path("search/", views.search_games, name="search"),
   path("add-game/", views.add_game, name="add_game"),
]