from django.urls import path
from . import views

urlpatterns=[
    
    path("func/",views.all_threads,name="directs"),
    path("make_thread/<str:username>/",views.makeThread,name="make_thread"),
    path("eachThread/<str:pk>/",views.EachThread.as_view(),name="eachThread"),
    path("sendMessage/<str:thread_id>/",views.sendMessage,name="sendMessage"),

]