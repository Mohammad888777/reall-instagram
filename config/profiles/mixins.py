from django.shortcuts import redirect,get_object_or_404
from django.http import Http404
from .models import Profile
from django.urls import reverse
from posts.models import Follow


class PrivateAccountSeeFollwersAndFollowings:

        def dispatch(self, request, *args, **kwargs) :

            username=self.kwargs.get("username")
            profile=get_object_or_404(Profile.objects.select_related("user").prefetch_related("favourite","follwer_requested"),user__username=username)
            
            if self.request.user==profile.user:
                return super().dispatch(request, *args, **kwargs)

            if profile.status=="private":
                f=Follow.objects.select_related("follower","following").filter(follower=self.request.user,following=profile.user,request_status="accepted").exists()
                if f:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    return redirect(self.request.META.get("HTTP_REFERER"))

          
            else:
                return super().dispatch(request, *args, **kwargs)







class LoginNeed():

    def dispatch(self,request,*args,**kwargs):

        if self.request.user.is_authenticated:
            return super().dispatch(request,*args,**kwargs)
        return redirect("custom_login")
    



class EditProfile():

    def dispatch(self,request,username,*args,**kwargs):

        profile=get_object_or_404(Profile,user__username=username)

        if self.request.user.is_authenticated:
                if self.request.user==profile.user:
                    return super().dispatch(request,username,*args,**kwargs)
                return reverse("myProfile",kwargs={"username":username})
        return redirect("custom_login")
    


        

