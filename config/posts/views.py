from django.shortcuts import render,redirect,get_object_or_404
from .models import Like,Follow,Post,Tag,Stream
from .decorators import login_need,see_streams
from .forms import PostForm
from django.http import HttpResponseRedirect,JsonResponse
from profiles.models import Profile
from accounts.models import User
from django_otp.decorators import otp_required





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
    
    contex={
        'post_items':post_items,
        'liked_post':liked_post,
        'saved_post':saved_post

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
        'saved':saved
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

    return JsonResponse({"like":l})


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

