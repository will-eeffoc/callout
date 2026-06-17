import secrets, requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, EmailAuthenticationForm, ProfileEditForm
from .models import Profile, Game
from chipin.models import Review
from chipin.forms import ReviewForm
from django.db.models import Avg

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

def _hp_name(request):
    # Generate a unique honeypot field name per session to block bots
    # Same name stays consistent throughout the session to help with form display
    if "hp_name" not in request.session:
        request.session["hp_name"] = f"hp_{secrets.token_hex(8)}"
    return request.session["hp_name"]

def login_view(request):
    # Handle user login with multiple security checks:
    # 1. Honeypot field to catch bots
    # 2. Timing guard to reject suspiciously fast submissions
    # 3. reCAPTCHA validation
    # 4. Finally check username/password
    hp_name = _hp_name(request)

    if request.method == "POST":
        # 1) Honeypot (cheap check first) - if this field is filled, it's a bot
        if request.POST.get(hp_name):
            messages.error(request, "Bot detected.")
            return redirect("users:login")

        # 2) Timing guard (humans rarely submit under 1.5s)
        try:
            elapsed = float(request.POST.get("elapsed", 0))
            if elapsed < 1.5:
                messages.error(request, "Please wait a moment before submitting.")
                return redirect("users:login")
        except (TypeError, ValueError):
            pass

        # 3) reCAPTCHA verify (network call after cheap checks)
        token = request.POST.get("recaptcha-token")
        data = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }
        try:
            resp = requests.post(RECAPTCHA_VERIFY_URL, data=data, timeout=3.0)
            result = resp.json()
        except requests.RequestException:
            result = {"success": False}

        if not result.get("success"):
            messages.error(request, "reCAPTCHA validation failed. Please try again.")
            return redirect("users:login")

        # 4) Authenticate user with email/password
        username = (request.POST.get("username") or "").strip().lower()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # rotate honeypot name after each successful POST
            request.session["hp_name"] = f"hp_{secrets.token_hex(8)}"
            next_url = request.GET.get("next", reverse("chipin:home"))
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("users:login")

    # GET: render with the current hp_name
    next_url = request.GET.get("next", "")
    return render(request, "users/login.html", {"hp_name": hp_name, "next": next_url})

def register(request):
    # Handle user registration - GET shows the form, POST creates a new account
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required(login_url='users:login')
def user(request):
    # This endpoint redirects logged-in users to the home page
    return render(request, "chipin/home.html")

def logout_view(request):
    # Log the user out and show a success message
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('users:login')

@login_required
def profile_view(request):
    # Display the current user's profile
    profile = request.user.profile
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    # Allow users to edit their profile info: name, nickname, bio, favorite games
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

def game_detail(request, game_id):
    # Show game details: description, reviews, average rating, and allow user to submit/edit their own review
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        messages.error(request, "Game not found.")
        return redirect('chipin:home')
    
    reviews = game.reviews.all()
    # Calculate the average rating across all reviews
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    user_review = None
    
    # Check if the logged-in user has already reviewed this game
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    # Handle review submission or update
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been saved!")
            return redirect('users:game_detail', game_id=game_id)
    else:
        form = ReviewForm(instance=user_review) if request.user.is_authenticated else None
    
    context = {
        'game': game,
        'reviews': reviews,
        'average_rating': average_rating,
        'user_review': user_review,
        'form': form,
    }
    return render(request, 'users/game_detail.html', context)