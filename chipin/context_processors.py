from users.models import Profile

def user_profile(request):
    # Make the user's nickname available in all templates
    # This allows templates to easily display personalized content
    if request.user.is_authenticated:
        try:
            return {'nickname': request.user.profile.nickname}
        except Profile.DoesNotExist:
            # Fallback to username if the profile doesn't exist yet (rare edge case)
            return {'nickname': request.user.username}
    return {}