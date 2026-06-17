from django.urls import path
from . import views

# URL routes for the users app (authentication and profiles)
urlpatterns = [
    path('login/', views.login_view, name='login'),  # User login with security checks
    path('logout/', views.logout_view, name='logout'),  # Logout and redirect to login
    path('register/', views.register, name='register'),  # New user registration
    path('profile/', views.profile_view, name='profile'),  # View current user's profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit profile info and favorite games
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),  # View game details and reviews
]