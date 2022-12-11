from django.urls import path
from . import views

urlpatterns=[
    
    path("login/",views.LoginView.as_view(),name="custom_login"),
    path("register/",views.Register.as_view(),name="custom_register"),
    path("activate/<uidb64>/<token>/",views.activate,name="activate"),
]