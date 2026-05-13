from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Game

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'
    fields = ('nickname', 'bio', 'favourite_game_1', 'favourite_game_2', 'favourite_game_3', 'favourite_game_4')
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user_username", "user_first_name", "user_last_name", "user_email", "nickname")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "nickname")

    def user_username(self, obj): return obj.user.username
    def user_first_name(self, obj): return obj.user.first_name
    def user_last_name(self, obj): return obj.user.last_name
    def user_email(self, obj): return obj.user.email

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)
