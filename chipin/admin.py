from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Django admin interface for managing game reviews
    # Display user, game, rating, and date in the list view
    # Allow filtering by rating and creation date
    # Enable searching by username and game title
    list_display = ('user', 'game', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'game__title')
    # Don't let admins edit the timestamps - they're auto-generated
    readonly_fields = ('created_at', 'updated_at')

