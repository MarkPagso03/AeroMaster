from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse


def role_required(required_role):
    """ Restrict access to specific roles """

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('login_admin'))
            if request.user.role != required_role:
                return HttpResponseForbidden("Access Denied.")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
