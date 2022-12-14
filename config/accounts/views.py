from django.shortcuts import render,redirect,get_object_or_404
from .models import User
from django.views import View
from django.contrib.auth import login,logout,authenticate
from .forms import LoginForm,RegisterForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts  import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required



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




@login_required(redirect_field_name="custom_login")
def logoutView(request):
    logout(request)
    return redirect("custom_login")



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

                    current_site=get_current_site(request)
                    subject="activate your account"
                    body=render_to_string("accounts/activate_account.html",{
                        "user":user,
                        "domin":current_site,
                        "uid":urlsafe_base64_encode(force_bytes(user.id)),
                        "token":default_token_generator.make_token(user)
                    })
                    mail=EmailMessage(subject=subject,body=body,to=[email])
                    mail.send()
                    
                    messages.success(request,"account is created")
                    return redirect("custom_login")
                messages.error(request,"username already exists")
                return redirect(self.request.META.get('HTTP_REFERER'))
            messages.error(request,"email already exists")
            return redirect(self.request.META.get('HTTP_REFERER'))

        messages.error(request,"form is not avlid")
        return redirect(self.request.META.get('HTTP_REFERER'))


def activate(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64)
        user=User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"your account is verfied successfully")
        return redirect("custom_login")
    else:
        messages.error(request,"your activation code is incorrect send again")
        return redirect("custom_register")




def forgotPassword(request):

    if request.method=="POST":
        email=request.POST.get("email")
        user=User.objects.filter(email=email)
        if user.exists():
            auth=User.objects.select_related("profile").prefetch_related("post_set").get(email__iexact=email)

            subject="reset password "
            current_site=get_current_site(request)
            body=render_to_string("accounts/forgotPasswodActivate.html",{
                "user":auth,
                "domin":current_site,
                "uid":urlsafe_base64_encode(force_bytes(auth.id)),
                "token":default_token_generator.make_token(auth)
            })
            mail=EmailMessage(subject=subject,body=body,to=[auth.email])
            mail.send()
            messages.success(request,"email is sent to reset your passowrd")
            return redirect("custom_login")
        messages.error(request,"user with this email does not exisit")
        return redirect(request.META.get("HTTP_REFERER"))
    return render(request,"accounts/forgotPassword.html")
        


def validateEmail(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(id=uid)
    except User.DoesNotExist:
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session["uid"]=uid
        return redirect("resetPassowrd")
    messages.error(request,"link is expired")
    return redirect("forgotPassword")



def resetPassowrd(request):

    if request.method=="POST":
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
        if password==confirm_password:
            user_id=request.session.get("uid")
            user=User.objects.get(id=user_id)
            if user:
                user.set_password(password)
                user.save()
                messages.success(request,"Your new Password is set")
                return redirect("custom_login")
            messages.error(request,"not user found")
        messages.error(request,"password does not match")
        return redirect(request.META.get("HTTP_REFERER"))
    return render(request,"accounts/resetPassword.html")
    