from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Transaction

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
