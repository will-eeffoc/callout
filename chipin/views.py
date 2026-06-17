from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Avg
from .forms import GameForm
from .models import Review
from users.models import Game

@login_required
def home(request):
    # Show the homepage with the 10 most recent reviews and newest games
    # We use select_related to avoid N+1 queries when loading game/user data
    recent_reviews = Review.objects.select_related('game', 'user').all()[:10]
    new_games = Game.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-created_at')[:10]
    return render(request, 'chipin/home.html', {'recent_reviews': recent_reviews, 'new_games': new_games})

@login_required
def search_games(request):
    # Search for games by title or description (case-insensitive)
    query = request.GET.get('q', '')
    results = []
    if query:
        # Use Q objects to search both title and description
        results = Game.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'chipin/search_results.html', {'results': results, 'query': query})

@login_required
def add_game(request):
    # Handle adding a new game - GET shows the form, POST saves it to the database
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Game added successfully!")
            return redirect('chipin:home')
    else:
        form = GameForm()
    return render(request, 'chipin/add_game.html', {'form': form})
