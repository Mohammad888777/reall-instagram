from functools import wraps
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import Like,Follow,Post,Tag,Stream
from .forms import PostForm
from django.http import HttpResponseRedirect,JsonResponse
from profiles.models import Profile
from accounts.models import User
from django.conf import settings




def see_streams(func):
    @wraps(func)
    def inner(request,*args,**kwargs):

        if request.user.is_authenticated:
            profile=get_object_or_404(Profile,user=request.user)
            # followers=Follow.objects.all().filter(following=user)
            if profile:
                return func(request,*args,**kwargs)
        return redirect("custom_login")
    return inner












def login_need(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        return redirect("custom_login")
    return inner