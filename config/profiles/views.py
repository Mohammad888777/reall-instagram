from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile
from django.views import View
from posts.models import Post,Follow
from .utils import handle_paginator
from .mixins import LoginNeed,EditProfile,PrivateAccountSeeFollwersAndFollowings
from .decorators import mixin_to_see_saved_post
from .forms import ProfileForm
from django.views.generic import UpdateView,ListView
from django.urls import reverse
from django.http import JsonResponse





class ProfileView(LoginNeed,View):

    def get(self,request,username,*args,**kwargs):
        
        page=self.request.GET.get("page",1)

        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite"),user__username=username)

        user_allowed=False

        if profile.status=="private":

            all_follows=Follow.objects.all()

            for i in all_follows:
                if i.follower==self.request.user and i.request_status =="accepted" and  i.following == profile.user:
                    user_allowed=True
                else:
                    user_allowed=False
        print(user_allowed)





        posts=Post.objects.select_related("user").filter(
            user=profile.user
        ).order_by("-posted")
        followers=Follow.objects.select_related('user').filter(
            following=profile.user
        )
        followings=Follow.objects.select_related("user").filter(
            follower=profile.user
        )
        

        followed=Follow.objects.select_related("user").filter(
            follower=self.request.user,following=profile.user
        ).exists()
        # print(followed)

        post_result=handle_paginator(posts,10,page)

        follow_status=None

        if self.request.user != profile.user:
            follow_status=Follow.objects.filter(follower=self.request.user,following=profile.user).exists()

        status_follow=None

        if follow_status:
            f=Follow.objects.get(follower=self.request.user,following=profile.user)
            status_follow=f.request_status

        print(status_follow)

        
        contex={

            'profile':profile,
            'posts':posts,
            'followers':followers,
            'followings':followings,
            'post_paginated':post_result,
            'followed':followed,
            'user_allowed':user_allowed,
            'status_follow':status_follow

        }

        return render(request,"profiles/profile.html",contex)




@mixin_to_see_saved_post
def saved_posts(request,username):
    
    profile=get_object_or_404(Profile.objects.select_related('user').prefetch_related("favourite")  ,user__username=username)
    posts_saved=profile.favourite.select_related("user").all()
    contex={
        'saved_posts':posts_saved
    }
    return render(request,"profiles/saved_posts.html",contex)





class UpdateProfile(LoginNeed,EditProfile,UpdateView):

    template_name: str="profiles/editProfile.html"
    model=Profile
    form_class=ProfileForm


    def get_object(self):

        k=self.kwargs.get("username")
        return Profile.objects.select_related("user").prefetch_related("favourite").get(
            user__username=k
        )

    def get_success_url(self) -> str:
        k=self.kwargs.get("username")
        return reverse("myProfile",kwargs={"username":k})





@mixin_to_see_saved_post
def make_account_private(request,username):

    profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite"),user__username=username)


    if profile.status=="public":
        profile.status="private"
    elif profile.status=="private":
        profile.status="public"
    status=profile.status
    profile.save()
    
    return JsonResponse({"status":profile.status})




@mixin_to_see_saved_post
def send_request(request,username):

    profile=Profile.objects.select_related("user").prefetch_related(
        "follwer_requested","favourite"
    ).get(user__username=username)

    fol=Follow.objects.filter( follower=request.user,following=profile.user,request_status="requested").exists()
    f=None

    if fol:

        f=Follow.objects.get(
            follower=request.user,following=profile.user,request_status="requested"
        )  
        if f:
            f.request_status="empty"
            f.save()
        
            return redirect(request.META.get("HTTP_REFERER"))
        
    elif not fol:

        new_f=Follow.objects.filter( follower=request.user,following=profile.user,request_status="empty").exists()

        if new_f:
                a=Follow.objects.get(follower=request.user,following=profile.user,request_status="empty")
                a.request_status="requested"
                a.save()
            
        else:
           
            Follow.objects.create(
            follower=request.user,following=profile.user,request_status="requested"
            )
            profile.follwer_requested.add(f)
            profile.save()

        


    return JsonResponse({"status":"requested"})




class Followers(PrivateAccountSeeFollwersAndFollowings,ListView):

    template_name: str="profiles/followers.html"

    def get_queryset(self) :
        
        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)

        followers=Follow.objects.select_related("follower","following").filter(
            following=profile.user
        )

        return followers
    
    def get_context_data(self, **kwargs) :

        contex= super().get_context_data(**kwargs)
        
        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)

        followers=Follow.objects.select_related("follower","following").filter(
            following=profile.user
        )

        followed_by_user=[]
        not_followed_by_user=[]

        for f in followers:
            for j in f.follower.following.all():
                if j.follower==self.request.user:
                    followed_by_user.append(j)
                else:
                    not_followed_by_user.append(j)
        print(followed_by_user)
        print(not_followed_by_user)

        contex["followed_by_user"]=followed_by_user
        contex["not_followed_by_user"]=not_followed_by_user



        return contex
        




class Followings(PrivateAccountSeeFollwersAndFollowings,ListView):

    template_name: str="profiles/followings.html"

    def get_queryset(self) :

        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)

        followings=Follow.objects.select_related("follower","following").filter(
            follower=profile.user
        )

        return followings
    


class Settings(LoginNeed,EditProfile,View):

    def get(self,request,username,*args,**kwargs):

        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)
        contex={
            'profile':profile
        }

        return render(request,"profiles/settings.html",contex)        



def follow(request,username):

    profile_to_follow=get_object_or_404(Profile,user__username=username)

    if profile_to_follow.status!="private":
        f=Follow.objects.filter(follower=request.user,following=profile_to_follow.user).exists()
        if not f:
            Follow.objects.create(
                follower=request.user,following=profile_to_follow.user
            )
            return JsonResponse({"followed":True})
        else:
            f=Follow.objects.filter(follower=request.user,following=profile_to_follow.user)
            f.delete()
            return JsonResponse({"followed":False})

    elif profile_to_follow.status == "private" and Follow.objects.filter(follower=request.user,following=profile_to_follow.user,request_status="accepted").exists():
            print("HHEEERRREEEE")
            f=Follow.objects.filter(follower=request.user,following=profile_to_follow.user)
            f.delete()
            return JsonResponse({"followed":False})

    elif profile_to_follow.status=="private" and not Follow.objects.filter(follower=request.user,following=profile_to_follow.user).exists():
        send_request(request,profile_to_follow.user.username)
    


    
