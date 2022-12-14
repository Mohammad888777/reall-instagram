from django.urls import path
from . import views

urlpatterns=[

        path("addComment/<str:post_id>/",views.addComment,name="addComment"),
        path("replayComment/<str:post_id>/<str:comment_id>/",views.commentReplay,name="replayComment"),
    
]