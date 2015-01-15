from django.contrib.auth.models import User

def get_user(username, defaults={}):
    """Given a username, gets or creates it in the local database and returns
    the User instance."""
    user, created = User.objects.get_or_create(username=username, defaults=defaults)
    return user
