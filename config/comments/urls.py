from django.urls import path
from . import views

urlpatterns=[

        path("addComment/<str:post_id>/",views.addComment,name="addComment"),
        path("addCommentIndex/<str:post_id>/",views.addCommentIndex,name="addCommentIndex"),
        path("replayComment/<str:post_id>/<str:comment_id>/",views.commentReplay,name="replayComment"),
        path("likeComment/<str:post_id>/<str:comment_id>/",views.likeComment,name="likeComment"),
    
]