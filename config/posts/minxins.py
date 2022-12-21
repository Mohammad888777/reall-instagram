from django.shortcuts import redirect,get_object_or_404
from profiles.models import Profile
from .models import Post


class PostEditMixin:

    def dispatch(self,request,*args,**kwargs):
        
        post=get_object_or_404(Post,pk=self.kwargs.get("pk"))
        if self.request.user.is_authenticated:
            if self.request.user==post.user:
                return super().dispatch(request,*args,**kwargs)
            return redirect("myProfile",self.request.user.username)
        return redirect("custom_login")