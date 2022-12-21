from django.urls import path
from . import views

urlpatterns=[

    path("<str:username>/",views.NotifificationsView.as_view(),name="notifications"),
    path("requested_followers/<str:username>/",views.notifs_for_private,name="requested_followers"),

]