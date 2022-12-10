from django.shortcuts import redirect
from functools import wraps
from .models import Profile


def mixin_to_see_saved_post(func):
    @wraps(func)
    def inner(request,username,*args,**kwargs):
        profile=Profile.objects.select_related("user").prefetch_related("favourite").get(
            user__username=username
        )
        if request.user.is_authenticated:
            if profile:
                return func(request,username,*args,**kwargs)
            return redirect("index")
        return redirect("index")
    return inner
