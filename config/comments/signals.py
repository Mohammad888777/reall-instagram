from django.db.models.signals import post_delete,post_save
from .models import Comment,CommentLike
from notifications.models import Notification




def send_notification_comment_like(sender,instance,created,**kwargs):
    print(instance.comment,"INSTANE     dasdasdasdadasd",instance.comment.user)

    if created:
        if instance.comment.is_parent:
            if instance.user != instance.comment.user:

                Notification.objects.create(
                    sender=instance.user,receiver=instance.comment.user,notification_types=6,comment=instance.comment,
                    post=instance.comment.post
                )
        

        


def delete_notification_comment_like(sender,instance,**kwargs):

    if instance.comment.is_parent:
        if instance.user != instance.comment.user:

            noti=Notification.objects.filter(
                sender=instance.user,receiver=instance.comment.parent.user,notification_types=6,comment=instance.comment,
                post=instance.comment.post
            )
            noti.delete()

post_save.connect(send_notification_comment_like,sender=CommentLike)
post_delete.connect(send_notification_comment_like,sender=CommentLike)




def send_notification_comment(sender,instance,created,**kwargs):
    
    if instance.post.user == instance.user:
        type_number1=None
        if instance.is_parent:
            type_number1=2
        else:
            type_number1=5
        
        if type_number1==5 and instance.user != instance.parent.user:
            Notification.objects.create(
                sender=instance.user,receiver=instance.parent.user,notification_types=5,comment=instance,post=instance.post
            )
    elif instance.post.user != instance.user:

        type_number2=None

        if instance.is_parent:
            type_number2=2
        else:
            type_number2=5

        if type_number2==2:

            Notification.objects.create(
                sender=instance.user,receiver=instance.post.user,notification_types=2,comment=instance,post=instance.post
            )
        elif type_number2==5:

            Notification.objects.create(
                sender=instance.user,receiver=instance.parent.user,notification_types=5,comment=instance,post=instance.post
            )


def delete_notification_comment(sender,instance,**kwargs):

    if instance.post.user == instance.user:
        type_number3=None
        if instance.is_parent:
            type_number3=2
        else:
            type_number3=5
        
        if type_number3==5:
           n= Notification.objects.filter(
                sender=instance.user,receiver=instance.parent.user,notification_types=5,comment=instance,post=instance.post
            )
           n.delete()

    elif instance.post.user != instance.user:
        type_number4=None
        if instance.is_parent: 
            type_number4=2
        else:
            type_number4=5

        if type_number4==2:

            n1=Notification.objects.filter(
                sender=instance.user,receiver=instance.post.user,notification_types=2,comment=instance,post=instance.post
            )
            n1.delete()

        elif type_number4==5:

            n2=Notification.objects.filter(
                sender=instance.user,receiver=instance.parent.user,notification_types=5,comment=instance,post=instance.post
            )
            n2.delete()
    

post_save.connect(send_notification_comment,sender=Comment)
post_delete.connect(delete_notification_comment,sender=Comment)