from django.shortcuts import render,redirect,get_object_or_404
from .models import Thread,Message
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import User
from profiles.models import Profile
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MessageForm




@login_required
def makeThread(request,username):

    r=get_object_or_404(User.objects.select_related('profile').prefetch_related('post_set'),username=username)
    u=get_object_or_404(User.objects.select_related('profile').prefetch_related('post_set'),username=request.user.username)

    thread=None
    print("$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$")
    print(r)
    print(u)
    print("$$$$$$$$$$$$$$$$$$$$$$$$")

    print("$$$$$$$$$$$$$$$$$$$$$$$$")

    threadOne=Thread.objects.select_related("sender","receiver").filter(
        receiver=r,sender=u
        )
    threadTwo=Thread.objects.select_related("sender","receiver").filter(
        receiver=u,sender=r
    )
    if threadOne.exists():
        thread=threadOne
    elif threadTwo.exists():
        thread=threadTwo
    else:
        thread=Thread.objects.select_related("sender","receiver").create(
         sender=u,receiver=r
        )
    print("Don")
    print(thread)
    
    return redirect("eachThread",thread.pk)
    






@login_required
def all_threads(request):

    threads=Thread.objects.select_related("sender","receiver").filter(
        Q(sender=request.user)|Q(receiver=request.user)
    )

    contex={
        'directs':threads
    }
    return render(request,"directs/all_directs.html",contex)






class EachThread(LoginRequiredMixin,View):

    def get(self,request,pk,*args,**kwargs):

        thread=Thread.objects.select_related("sender","receiver").get(
            pk=pk
        )
        thread.is_seen=True
        thread.save()
        messages=Message.objects.select_related("thread","receiver_user","sender_user").filter(
            # Q(sender_user=thread.sender,receiver_user=thread.receiver)|Q(sender_user=thread.receiver,receiver_user=thread.sender)
            thread=thread
        )
        contex={
            'messages':messages,
            'thread':thread,
            'form':MessageForm
        }
        return render(request,"directs/eachThread.html",contex)

    
    


def sendMessage(request,thread_id):

    if request.method=="POST":

        thread=get_object_or_404(Thread,pk=thread_id)

        # form=MessageForm(request.POST or None,request.FILES or None)
        body=request.POST.get("body")
        image=request.FILES["image"]
        print(body,image)

        if thread.receiver == request.user:
            receiver=thread.sender
        else:
            receiver=thread.receiver
        print("RRRRREEECER",receiver)

        # msg=[]
        new_message=Message(sender_user=request.user,receiver_user=receiver,body=body,image=image,thread=thread)
        new_message.save()
        message=Message.objects.select_related("thread","sender_user","receiver_user").get(id=new_message.id)
        
        msg=[

                {
                    "body":message.body,
                    "image":message.image.url,
                    # "sender_user":message.sender_user,
                    # "receiver_user":message.receiver_user,
                    # "thread":message.thread
                    "id":message.id,
                    "imageProfile":message.sender_user.profile.image.url,
                    "date":message.date
                }
        ]


        if request.is_ajax():
            return JsonResponse(msg,safe=False)
        print("NOt valid ")
        return redirect("eachThread",thread.pk)

