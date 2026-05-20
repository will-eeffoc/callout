from django import forms
from users.models import Game

class GameForm(forms.ModelForm):
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
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Game title is required.")
        # Check if a game with this title already exists (case-insensitive)
        if Game.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A game with this title already exists.")
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError("Game description is required.")
        return description
    
    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if not cover:
            raise forms.ValidationError("A cover image is required.")
        # Validate file size (max 5MB)
        if cover.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size must not exceed 5MB.")
        return cover
