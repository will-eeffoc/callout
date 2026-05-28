from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GameForm

@login_required
def home(request):
    return render(request, 'chipin/home.html')

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
