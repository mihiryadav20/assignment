from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated
from social_django.models import UserSocialAuth
from .models import UserProfile

def social_user_with_email_fallback(backend, uid, user=None, *args, **kwargs):
    """
    Custom pipeline function to handle the case where a social account is already associated with another user.
    This will try to find a user with the same email and use that instead.
    """
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    
    if social:
        # If this social account is already associated with a user
        if user and social.user != user:
            # If we're trying to associate with a different user, check if emails match
            email = kwargs.get('details', {}).get('email')
            if email:
                try:
                    existing_user = get_user_model().objects.get(email=email)
                    if existing_user == social.user:
                        # The emails match, so we can use this user
                        return {'social': social, 'user': social.user}
                    else:
                        # Disconnect the social account from the old user
                        social.user = None
                        social.save()
                except get_user_model().DoesNotExist:
                    pass
        else:
            # Normal case - social account matches current user
            return {'social': social, 'user': social.user}
    return {}

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
