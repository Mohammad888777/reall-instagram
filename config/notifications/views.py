from django.shortcuts import render,redirect,get_object_or_404
from .models import Notification
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Follow
from profiles.models import Profile



class NotifificationsView(LoginRequiredMixin,ListView):

    template_name: str="notifications/notifications.html"

    def get_queryset(self):
        # global notis
        username=self.kwargs.get("username")
        notis=Notification.objects.select_related( 'post', 'sender', 'receiver').filter(
            receiver__username=username
        )

        return notis

    def dispatch(self, request,username, *args, **kwargs) :
        notis=Notification.objects.select_related( 'post', 'sender', 'receiver').filter(
            receiver__username=username
        )
        

        if self.request.user.is_authenticated:
            for n in notis:
                if self.request.user == n.receiver:
        
                    return super().dispatch(request,username, *args, **kwargs)
                else:
                    return redirect("myProfile",self.request.user.username)
        return redirect("custom_login")
    

    def get_context_data(self, **kwargs) :

        username=self.kwargs.get("username")
        contex=super().get_context_data(**kwargs)
        profile=Profile.objects.select_related("user").prefetch_related(
            "favourite","follwer_requested"
        ).get(user__username=username)

        profile_status=profile.status
        # all_f=Follow.objects.select_related("follower","following").filter(
        #     following=profile.user
        # )
        contex["profile_status"]=profile_status
        return contex