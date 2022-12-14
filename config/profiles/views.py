from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile
from django.views import View
from posts.models import Post,Follow
from .utils import handle_paginator
from .mixins import LoginNeed,EditProfile,PrivateAccountSeeFollwersAndFollowings
from .decorators import mixin_to_see_saved_post
from .forms import ProfileForm,EditProfile
from django.views.generic import UpdateView,ListView
from django.urls import reverse
from django.http import JsonResponse
from accounts.models import User
from django.contrib import messages
from django.db.models import Q



class ProfileView(LoginNeed,View):

    def get(self,request,username,*args,**kwargs):
        
        page=self.request.GET.get("page",1)

        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)

        user_allowed=False

        if profile.status=="private":

            all_follows=Follow.objects.all()

            for i in all_follows:
                if i.follower==self.request.user and i.request_status =="accepted" and  i.following == profile.user:
                    user_allowed=True
                else:
                    user_allowed=False
        print(user_allowed)



        user_followed_no_private_status=None
        if profile.status!="private":
            ff=Follow.objects.select_related("follower","following").filter(follower=self.request.user,following=profile.user,request_status ="empty").exists()
            if ff:
                
                user_followed_no_private_status="Following"
            else:
                user_followed_no_private_status="Follow"



        posts=Post.objects.select_related("user").filter(
            user=profile.user
        ).order_by("-posted")

        filtred_Followers=[]

        followers=None
        if profile.status=="private":
            followers=Follow.objects.select_related("follower","following").filter(
            following=profile.user,request_status="accepted"
            )
            filtred_Followers.append(followers)
        elif profile.status=="public":
            followers=Follow.objects.select_related("follower","following").filter(
                following=profile.user
                )
            filtred_Followers.append(followers)
        
        
            
        


        # followings=None

        followings=Follow.objects.select_related("follower","following").filter(
            follower=profile.user
        )


        all_pis=[]

        for i in followings:
            p=Profile.objects.get(user=i.following)
            all_pis.append(p)
        
        filtred_following=[]

       
        fff=None
        for i in all_pis:
            if i.status=="private":
                fff=Follow.objects.select_related("follower","following").filter(
                    follower=profile.user,following=i.user,request_status="accepted"
                )
                filtred_following.append(fff)
            elif i.status=="public":

                fff=Follow.objects.select_related("follower","following").filter(
                    follower=profile.user,following=i.user
                    )
                filtred_following.append(fff)
        print("FILTREDDDDD",len(filtred_Followers),filtred_Followers)
        

        followed=Follow.objects.select_related("follower","following").filter(
            follower=self.request.user,following=profile.user
        ).exists()
        # print(followed)

        post_result=handle_paginator(posts,10,page)

        follow_status=None

        if self.request.user != profile.user:
            follow_status=Follow.objects.select_related("follower","following").filter(follower=self.request.user,following=profile.user).exists()

        status_follow=None

        if follow_status:
            f=Follow.objects.select_related("follower","following").get(follower=self.request.user,following=profile.user)
            status_follow=f.request_status

        # print(status_follow)
        # print("FOLOOOOWINGGG",fff)
        
        contex={

            'profile':profile,
            'posts':posts,
            'followers':followers,
            # 'followers_len':len(filtred_Followers),
            'followings':followings,
            # 'followings_len':len(filtred_following),
            'post_paginated':post_result,
            'followed':followed,
            'user_allowed':user_allowed,
            'status_follow':status_follow,
            'user_followed_no_private_status':user_followed_no_private_status,
            "profile_stat":"public" if  profile.status =="private" else "private"

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





class UpdateProfile(UpdateView):

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
    
    def dispatch(self, request, *args, **kwargs) :

        k=self.kwargs.get("username")
        profile=Profile.objects.select_related("user").prefetch_related("favourite").get(
            user__username=k
        )
        if self.request.user.is_authenticated:
            if self.request.user==profile.user:
                return super().dispatch(request, *args, **kwargs)
            return redirect("myProfile",self.request.user.username)
        return redirect("custom_login")
    





@mixin_to_see_saved_post
def make_account_private(request,username):

    profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite"),user__username=username)
    followers=Follow.objects.select_related("follower","following").filter(
        following=profile.user
    )

    if profile.status=="public":
        profile.status="private"
    elif profile.status=="private":
        profile.status="public"
        for f in followers:
            f.request_status="empty"
            f.save()
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
            # f.request_status="empty"
            # f.save()
            f.delete()
        
            return redirect(request.META.get("HTTP_REFERER"))
        
    elif not fol:

        
        new_f=Follow.objects.filter( follower=request.user,following=profile.user,request_status="empty").exists()

        if new_f:
                
                a=Follow.objects.get(follower=request.user,following=profile.user,request_status="empty")
                a.request_status="requested"
                a.save()
                if not request.is_ajax():
                    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
                    return redirect(request.META.get("HTTP_REFERER"))
            
        else:
            f=Follow.objects.create(
            follower=request.user,following=profile.user,request_status="requested"
            )
            profile.follwer_requested.add(f)
            profile.save()
            if not request.is_ajax():
                print("FFFFFFFFFFFFFFFFFFFFFFFFFFFF")

                return redirect(request.META.get("HTTP_REFERER"))
            


    return JsonResponse({"status":"requested"})


@mixin_to_see_saved_post
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
            print("ACCCCCEEPPPPTESSDDD")
            f=Follow.objects.filter(follower=request.user,following=profile_to_follow.user)
            f.delete()
            return JsonResponse({"followed":False})

    elif profile_to_follow.status=="private" and not Follow.objects.filter(follower=request.user,following=profile_to_follow.user).exists():
        # print("")
        print("HHEEERRREEEE")
        send_request(request,profile_to_follow.user.username)
    



class Followers(PrivateAccountSeeFollwersAndFollowings,ListView):

    template_name: str="profiles/followers.html"

    def get_queryset(self) :
        global username,profile,followers

        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)

        followers=Follow.objects.select_related("follower","following").filter(
            following=profile.user
        )

        return followers
    
    def get_context_data(self, **kwargs) :
        

        contex= super().get_context_data(**kwargs)
        users=[]
        for i in followers:
            u=User.objects.get(username=i.follower.username)
            users.append(u)
        print(users)

        contex["users"]=users
        return contex
        





class Followings(PrivateAccountSeeFollwersAndFollowings,ListView):

    template_name: str="profiles/followings.html"

    def get_queryset(self) :

        global username,profile,followings
        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)

        followings=Follow.objects.select_related("follower","following").filter(
            follower=profile.user
        )


        return followings


    def get_context_data(self, **kwargs):

        contex= super().get_context_data(**kwargs)
        users=[]
        for i in followings:
            u=User.objects.get(username=i.following.username)
            users.append(u)
        print(users)

        contex["users"]=users

        return contex
    
    



class Settings(View):

    def get(self,request,username,*args,**kwargs):

        profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)
        contex={
            'profile':profile,
            'form':EditProfile(instance=profile)
        }

        return render(request,"profiles/settings.html",contex)

    def post(self,request,*args,**kwargs):

        # profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)
        ProfileF=ProfileForm(self.request.POST,self.request.FILES)
        # print(ProfileF)
        if ProfileF.is_valid():
            pf=ProfileF.save(commit=False)
            pf.profile=self.request.user
            ProfileF.save()
            return redirect(self.request.META.get("HTTP_REFERER"))
        print(ProfileF.errors)
        return JsonResponse({"error":"not valid"})

    def dispatch(self, request, *args, **kwargs) :

        k=self.kwargs.get("username")
        profile=Profile.objects.select_related("user").prefetch_related("favourite").get(
            user__username=k
        )
        if self.request.user.is_authenticated:
            if self.request.user==profile.user:
                return super().dispatch(request, *args, **kwargs)
            return redirect("myProfile",self.request.user.username)
        return redirect("custom_login")


        






@mixin_to_see_saved_post
def change_password(request,username):

    profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("follwer_requested","favourite"),user__username=username)

    user=get_object_or_404(User,username=profile.user.username)
    if request.method=="POST":

        current_pass=request.POST.get("current_password")
        new_password=request.POST.get("new_password")
        confirm_password=request.POST.get("confirm_password")


        if user.check_password(current_pass):
            if new_password==confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request,"New Password Is Set")
                return redirect(request.META.get("HTTP_REFERER"))
            messages.error(request,"not match password")
            return redirect(request.META.get("HTTP_REFERER"))
        messages.error(request,"current password is not orrect")
        return redirect(request.META.get("HTTP_REFERER"))




 


def acceptFollower(request,username):

    profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user=request.user)

    user_want_to_follow=get_object_or_404(User.objects.select_related("profile").prefetch_related("post_set"),username=username)



    f=Follow.objects.select_related("follower","following").get(
        following=request.user,follower=user_want_to_follow,request_status="requested"
    )

    f.request_status="accepted"
    f.save()

    if not request.is_ajax():
        return redirect("requested_followers",profile.user.username)
    
    return JsonResponse({
        "accepted":True
    })





def rejectFollower(request,username):

    profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user=request.user)

    user_want_to_follow=get_object_or_404(User.objects.select_related("profile").prefetch_related("post_set"),username=username)



    f=Follow.objects.select_related("follower","following").get(
        following=request.user,follower=user_want_to_follow,request_status="requested"
    )

    f.request_status="rejected"
    f.save()

    if not request.is_ajax():
        return redirect("requested_followers",profile.user.username)
    
    return JsonResponse({
        "accepted":True
    })





def searchUser(request):
    profile("ASDASDASDASDASDASD")

    q=request.GET.get("term")
    query=Profile.objects.filter(Q(first_name__icontains=q)|Q(user__username__icontains=q))
    z=[i.user.username for i in query]
    
    return JsonResponse(z,safe=False)





def test(request):
    contex={
        'users':User.objects.all()
    }
    return render(request,"profiles/test.html",contex)