from django.urls import path
from . import views

urlpatterns=[
    
    path("login/",views.LoginView.as_view(),name="custom_login"),
    path("register/",views.Register.as_view(),name="custom_register"),
    path("logout/",views.logoutView,name="custom_logout"),
    path("forgotPassword/",views.forgotPassword,name="forgotPassword"),
    path("resetPassowrd/",views.resetPassowrd,name="resetPassowrd"),
    path("activate/<uidb64>/<token>/",views.activate,name="activate"),
    path("validateEmail/<uidb64>/<token>/",views.validateEmail,name="validateEmail"),
]