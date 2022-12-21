from django.shortcuts import render,redirect,get_object_or_404
from .models import Like,Follow,Post,Tag,Stream
from .decorators import login_need,see_streams
from .forms import PostForm
from django.http import HttpResponseRedirect,JsonResponse
from profiles.models import Profile
from accounts.models import User
from django_otp.decorators import otp_required
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib import messages
from comments.models import Comment
from comments.forms import CommentForm
from django.db.models import Q,Count
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .minxins import PostEditMixin
from django.urls import reverse




@see_streams
@login_need
def index(request):

    # all_user_follow=Follow.objects.filter(follower=request.user)
    # posts=Post.objects.filter(user__follower__in=all_user_follow)
    # print(all_user_follow)    for posts before made stream


    posts=Stream.objects.select_related("user","following","post").filter(user=request.user)

    group_ids=[]
    for post  in posts:
        group_ids.append(post.post.id)
    # print(group_ids)
    post_items=Post.objects.select_related("user").filter(
        id__in=group_ids
    ).order_by("-posted")

    liked_post=[]
    for post in post_items:
        for like  in post.post_likes.all():
            if like.user== request.user:
                liked_post.append(post)
    
    profile=get_object_or_404(Profile,user=request.user)


    saved_post=[]
    for post in profile.favourite.all():
        saved_post.append(post)
    
    commentIsLiked=[]
    for post in post_items:
        for com in post.comment_set.all():
            for like in com.comment_likes.all():
                if like.user==request.user:
                    commentIsLiked.append(com)

    

    # all_comments=[]
    # for post in post_items:
    #     for comment in post.comment_set.all():

    
    contex={
        
        'post_items':post_items,
        'liked_post':liked_post,
        'saved_post':saved_post,
        'commentForm':CommentForm,
        'commentIsLiked':commentIsLiked

    }

    return render(request,"posts/index.html",contex)



@see_streams
@login_need
def newPost(request):

    tags_obj=[]

    if request.method=="POST":
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            caption=form.cleaned_data.get("caption")
            picture=form.cleaned_data.get("picture")
            tags=form.cleaned_data.get("tags")
            tag_list=list(tags.split(","))
            for tag in tag_list:
                t,created=Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p,created=Post.objects.get_or_create(caption=caption,picture=picture,user=request.user)
            p.tags.add(*tags_obj)
            p.save()
 
            return redirect("index")
    contex={'form':PostForm}
    return render(request,"posts/newpost.html",contex)



def postDetail(request,post_id):

    post=get_object_or_404(Post,id=post_id)
    last_liked=Like.objects.filter(post=post).last()
    comments=Comment.objects.select_related("user","post").prefetch_related("tags"
    
    ) .filter(
        post=post
    ).order_by("likes","-created")

    # c=Comment.objects.get(id=55)
    # childs=[]
    # for i in c.children:
    #     childs.append(i)
    # print(childs)
    # tags=[]
    # if c.tags.all():
    #     for tag in c.tags.all():
    #         tags.append(tag)
    # print(tags)

    likedComment=[]
    all_comments=Comment.objects.select_related("user","post").prefetch_related("tags").filter(
        post=post
    ).order_by("likes","-created")
    for c in all_comments:
        for j in c.comment_likes.all():
            if j.user==request.user:
                likedComment.append(c)
    
    # for i in likedComment:
    #     if i in all_comments:
    #         print(i,"IIIIIIIIIIIII")
    # print(likedComment,"LIKEDDDD COMMENT")
    # print(all_comments,"ALL COMME")

    





    liked=False
    for like in post.post_likes.all():
        if request.user == like.user:
            liked=True
    
    profile=Profile.objects.prefetch_related("favourite").select_related("user").all()

    saved=False
    for i in profile:
        for p in i.favourite.all():
            if p == post:
                saved=True
    print(saved)



    contex={
        
        'post':post,
        'liked':liked,
        'saved':saved,
        'commentForm':CommentForm(),
        'last_liked':last_liked,
        'comments':comments,
        'likedComment':likedComment
    }
    return render(request,"posts/postDetail.html",contex)




def tags(request,tag_slug):

    tag=get_object_or_404(Tag,slug=tag_slug)
    posts=Post.objects.select_related("user").prefetch_related(
    ).filter(tags=tag)
    contex={
        'tag':tag,
        'posts':posts
    }
    return render(request,'posts/tags.html',contex)





@login_need
@see_streams
def like(request,post_id):

    post=get_object_or_404(Post,id=post_id)
    current_like=post.likes
    l=Like.objects.filter(post=post,user=request.user).exists()
    if not l:
        like=Like.objects.create(user=request.user,post=post)
        current_like+=1
    else:
        l2=Like.objects.get(user=request.user,post=post)
        l2.delete()
        current_like-=1

    post.likes=current_like
    post.save()
    # return HttpResponseRedirect(f"/post/{post.id}")

    return JsonResponse({"like":l,'current_like':current_like})


@login_need
@see_streams
def save_post(request,post_id):

    post=get_object_or_404(Post,id=post_id)
    profile=Profile.objects.get(user=request.user)
    # if profile.favourite.
    saved=False
    for p in profile.favourite.all() :
        if p == post:
            saved=True
        else:
            saved=False
    
    if not saved:
        profile.favourite.add(post)
    else:
        profile.favourite.remove(post)
    
    return JsonResponse({"saved":saved})





def likesView(request,post_id):

    post=get_object_or_404(Post,pk=post_id)
    likes_info=Like.objects.filter(post=post)
    users=[]
    for i in likes_info:
      
        # if request.user !=i.user:
            u=User.objects.get(username=i.user.username)
            users.append(u)

    # profiles=[]
    # for user in users:
    #     ps=Profile.objects.get(user=user)
    #     profiles.append(ps)

    # followed=[]
    # not_followed=[]
    # for user in users:
    #     f=Follow.objects.select_related("follower","following").filter(follower=request.user,following=user)
    #     if f.exists():
    #         followed.append(f)
    #     else:
    #         not_followed.append(f)
    

    # print(not_followed,"$$$$$$$$$$$$")
    # for i in users:
    #     for j in i.follower.all():
    #         print(j)

    contex={
        # 'object_list':profiles,
        # 'followed':followed,
        # 'not_followed':not_followed,
        'users':users
    }
 
    return render(request,"posts/likesView.html",contex)








class EditPost(LoginRequiredMixin,PostEditMixin,UpdateView):

    template_name: str="posts/editPost.html"
    model=Post
    fields=["picture","caption","tags"]
    
    def get_success_url(self) -> str:

        return reverse("myProfile",kwargs={"username":self.request.user.username})
    
