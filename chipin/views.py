from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import GameForm
from .models import Review
from users.models import Game

@login_required
def home(request):
    recent_reviews = Review.objects.select_related('game', 'user').all()[:10]
    return render(request, 'chipin/home.html', {'recent_reviews': recent_reviews})

@login_required
def search_games(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Game.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'chipin/search_results.html', {'results': results, 'query': query})

@login_required
def add_game(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Game added successfully!")
            return redirect('chipin:home')
    else:
        form = GameForm()
    return render(request, 'chipin/add_game.html', {'form': form})
