from .models import User

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == "facebook":
        User.objects.get(user).update(avatar=response['user']['picture'])
