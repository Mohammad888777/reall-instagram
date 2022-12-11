from django.urls import path
from . import views

urlpatterns=[

    path("<str:username>/",views.ProfileView.as_view(),name="myProfile"),
    path("saved_posts/<str:username>/",views.saved_posts,name="saved_posts"),
    path("edit_profile/<str:username>/",views.UpdateProfile.as_view(),name="edit_profile"),
    path("make_account_private/<str:username>/",views.make_account_private,name="make_account_private"),
    path("send_request/<str:username>/",views.send_request,name="send_request"),
    path("followers/<str:username>/",views.Followers.as_view(),name="followers"),
    path("followings/<str:username>/",views.Followings.as_view(),name="followings"),
    path("settings/<str:username>/",views.Settings.as_view(),name="settings"),
    path("change_password/<str:username>/",views.change_password,name="change_password"),
    path("follow/<str:username>/",views.follow,name="follow"),

]