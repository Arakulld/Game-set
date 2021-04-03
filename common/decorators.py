from django.contrib.auth.models import User
from django.shortcuts import redirect
from functools import wraps


def not_auth(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        user: User = request.user
        if user.is_authenticated:
            return redirect('index')
        return f(request, *args, **kwargs)

    return wrapper
