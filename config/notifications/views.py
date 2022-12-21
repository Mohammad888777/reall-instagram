from django.shortcuts import render,redirect,get_object_or_404
from .models import Notification
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Follow
from profiles.models import Profile
from accounts.models import User


class NotifificationsView(LoginRequiredMixin,ListView):

    template_name: str="notifications/notifications.html"

    def get_queryset(self):
        # global notis
        username=self.kwargs.get("username")
        notis=Notification.objects.select_related( 'post', 'sender', 'receiver').filter(
            receiver__username=username
        
        ).order_by("-date")
        for i in notis:
            i.is_seen=True
            i.save()
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

        last_follow=Notification.objects.select_related( 'post', 'sender', 'receiver').filter(
            receiver__username=username,notification_types=3,
        
        ).order_by("-date")


        profile=Profile.objects.select_related("user").prefetch_related(
            "favourite","follwer_requested"
        ).get(user__username=username)

        profile_status=profile.status

        # last_follow

        all_f=Follow.objects.select_related("follower","following").filter(
            following=profile.user,request_status="requested"
        )
        
        contex["profile_status"]=profile_status
        contex["follow_requested"]=last_follow.count()
        contex["last_follow"]=last_follow.last()
        contex["all_f"]=all_f.last()
        contex["all_f_count"]=all_f.count()


        return contex
    



def notifs_for_private(request,username ):

    profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)
    followers=[]
    for follow in profile.follwer_requested.all():
        if follow.following == profile.user and follow.request_status =="requested" :
            followers.append(follow)
    print(followers)
    contex={
        'followers':followers,
        'profile':profile
    }
    return render(request,"notifications/private_requests.html",contex)
        
