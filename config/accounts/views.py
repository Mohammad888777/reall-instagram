from django.shortcuts import render,redirect,get_object_or_404
from .models import User
from django.views import View
from django.contrib.auth import login,logout,authenticate
from .forms import LoginForm,RegisterForm
from django.contrib import messages
from django.http import HttpResponseRedirect



class LoginView(View):

    def get(self,request,*args,**kwargs):

        contex={
            'form':LoginForm
        }

        return render(request,"accounts/login.html",contex)
    

    def post(self,request,*args,**kwargs):

        form=LoginForm(self.request.POST)
  
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")

            try:
                user=User.objects.get(username=username)
            except User.DoesNotExist:
                user=None
            print(user)
            if user:
                auth=authenticate(email=user.email,password=password)
                print(auth,"AUTHHTHTHTHTHTHTHTHAHHDJAHSDKASDADAD")
                if  auth is not None:
                    login(request,auth)
                    messages.success(request,"logged in successfully")
                    return redirect("myProfile",self.request.user.username)
                else:
                    messages.error(request,"user does not found")
                    return redirect("custom_login")
            else:
                messages.error(request,"username or password is invalid")
                return redirect("custom_login")
        print("NOOOOOOOOOOOOOOOOOO")
        messages.error(request,"user does not found")
        return redirect("custom_login")    


def logout(request):
    logout(request)
    return redirect("")


class Register(View):

    def get(self,request,*args,**kargs):
        contex={
            'form':RegisterForm()
        }
        return render(request,"accounts/register.html",contex)
    
    def post(self,request,*args,**kwargs):

        form=RegisterForm(self.request.POST)
        if form.is_valid():
            
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            password=form.cleaned_data.get("password")
            if not User.objects.filter(email=email).exists():
                if not User.objects.filter(username=username).exists():
                    user=User.objects.create_user(
                        first_name=username,last_name="...",password=password,
                        email=email,username=username
                    )
                    user.is_active=True
                    user.save()
                    messages.success(request,"account is created")
                    return redirect("custom_login")
                messages.error(request,"username already exists")
                return redirect(self.request.META.get('HTTP_REFERER'))
            messages.error(request,"email already exists")
            return redirect(self.request.META.get('HTTP_REFERER'))

        messages.error(request,"form is not avlid")
        return redirect(self.request.META.get('HTTP_REFERER'))