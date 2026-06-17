from django.urls import path
from . import views

# URL routes for the chipin app (game reviews and management)
urlpatterns = [
   path("", views.home, name="home"),  # Homepage showing recent reviews and new games
   path("search/", views.search_games, name="search"),  # Search for games by title or description
   path("add-game/", views.add_game, name="add_game"),  # Add a new game to the database
]