from django.urls import path
from . import views

urlpatterns=[
    
    path("",views.index,name="index"),
    path("add_post/",views.newPost,name="add_post"),
    path("post/<str:post_id>/",views.postDetail,name="postDetail"),
    path("editPost/<str:pk>/",views.EditPost.as_view(),name="editPost"),
    path("tags/<slug:tag_slug>/",views.tags,name="tags"),
    path("like_post/<str:post_id>/",views.like,name="like_post"),
    path("save_post/<str:post_id>/",views.save_post,name="save_post"),
    # path("addComment/<str:post_id>/",views.addComment,name="addComment"),
    path("likesView/<str:post_id>/",views.likesView,name="likesView"),

]