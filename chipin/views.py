from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Transaction
from .forms import GameForm

@login_required
def home(request):
    user = request.user
    profile = request.user.profile
    # get user's transaction history (newest first)
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-created_at')
    context = {
        'balance': profile.balance,
        'transactions': transactions,
    }
    return render(request, 'chipin/home.html', context)

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
