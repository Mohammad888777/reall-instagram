from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment
from .forms import CommentForm
from posts.models import Post
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.core import serializers



def addComment(request,post_id):
    
    post=get_object_or_404(Post.objects.select_related("user").prefetch_related("comment_set","tags"),pk=post_id)

    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=post
            new_comment.save()
            new_comment.create_tags()
            c=Comment.objects.select_related("user","post").prefetch_related("tags").get(
                id=new_comment.id
            )
            tags=[]
            if c.tags.all():
                for tag in c.tags.all():
                    tags.append(tag)
            print(tags)

            childrens=[]
            if  c.children:
                for child in c.children:
                    childrens.append(child)

           
            xx=[
                {"username":c.user.username,
                "profileImg":c.user.profile.image.url,
                "body":c.body,"created":c.created,
                "id":c.id,'tags':tags,
                "is_parent":c.is_parent,
                'childrens':childrens
                }
                ]
            print(xx)
            # data = serializers.serialize('json',xx )
            # return HttpResponse(data, content_type="application/json")
            return JsonResponse(xx,safe=False)
        print("NOTTTT VALIDDDD")
        messages.error(request,"not valid comment")
        return redirect("postDetail",post.pk) 




def commentReplay(request,post_id,comment_id):

    post=get_object_or_404(Post.objects.select_related("user").prefetch_related("tags","comment_set"),id=post_id)
    comment=get_object_or_404(Comment.objects.select_related("user","post").prefetch_related("tags"),id=comment_id)
    if request.method=="POST":
        print("YEES SPOOOSTTT")
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=post
            new_comment.parent=comment
            new_comment.save()

            tags=[]
            if new_comment.tags.all():
                for tag in new_comment.tags.all():
                    tags.append(tag)
            print(tags)

            xx=[
                {"username":new_comment.user.username,
                "profileImg":new_comment.user.profile.image.url,
                "body":new_comment.body,"created":new_comment.created,
                "id":new_comment.id,'tags':tags,
                # "is_parent":new_comment.is_parent
                }
                ]


            return JsonResponse(xx,safe=False)