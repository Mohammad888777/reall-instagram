from django.urls import path
from . import views

urlpatterns=[

    path("<str:username>/",views.NotifificationsView.as_view(),name="notifications"),

]