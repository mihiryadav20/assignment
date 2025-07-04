from .models import UserProfile

def create_reporter_profile(backend, user, response, *args, **kwargs):
    """
    Pipeline function to create a UserProfile with REPORTER role
    for users who authenticate via Google OAuth.
    """
    # Check if user already has a profile
    if not hasattr(user, 'profile'):
        # Create a new profile with REPORTER role
        UserProfile.objects.create(
            user=user,
            role=UserProfile.REPORTER
        )
        return {'is_new_reporter': True}
    
    return {'is_new_reporter': False}
