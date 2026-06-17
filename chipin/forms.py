from django import forms
from users.models import Game
from .models import Review

class GameForm(forms.ModelForm):
    # Form for adding or editing games with title, description, and cover image
    class Meta:
        model = Game
        fields = ['title', 'description', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter game title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter game description',
                'rows': 4
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_title(self):
        # Validate title: ensure it's not empty and is unique (case-insensitive)
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Game title is required.")
        # Check if a game with this title already exists (case-insensitive)
        if Game.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A game with this title already exists.")
        return title
    
    def clean_description(self):
        # Make sure there's actually a description
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError("Game description is required.")
        return description
    
    def clean_cover(self):
        # Validate the cover image: must exist and be under 5MB
        cover = self.cleaned_data.get('cover')
        if not cover:
            raise forms.ValidationError("A cover image is required.")
        # Validate file size (max 5MB)
        if cover.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size must not exceed 5MB.")
        return cover


class ReviewForm(forms.ModelForm):
    # Form for users to submit or edit their game reviews with a rating and text
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES, attrs={
                'class': 'rating-input'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about this game...',
                'rows': 4
            })
        }

