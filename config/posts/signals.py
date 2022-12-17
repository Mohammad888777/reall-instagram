from django.db.models.signals import post_delete,post_save
from .models import Like,Follow,Post
from accounts.models import User
from notifications.models import Notification

def send_notification_like(sender,instance,created,**kwargs):


    post=instance.post
    user=instance.user

    if instance.user != instance.post.user:
        Notification.objects.create(
            post=post,sender=user,receiver=post.user,notification_types=1
        )








def delete_notification_unlike(sender,instance,**kwargs):

    post=instance.post
    user=instance.user
    if instance.user != instance.post.user:
        noti=Notification.objects.filter(
        sender=user,receiver=post.user,notification_types=1,post=post
        )
        noti.delete()



def send_notification_follow(sender,instance,created,**kwargs):

    user=instance.follower
    receiver=instance.following
    if created:
        noti=Notification(
        sender=user,receiver=receiver,notification_types=3
        )
        noti.save()
    


def delete_notification_unfollow(sender,instance,**kwargs):

    user=instance.follower
    receiver=instance.following
    n=Notification.objects.filter(
        sender=user,receiver=receiver,notification_types=3
    )
    n.delete()





post_save.connect(send_notification_like,sender=Like)
post_delete.connect(delete_notification_unlike,sender=Like)



post_save.connect(send_notification_follow,sender=Follow)
post_delete.connect(delete_notification_unfollow,sender=Follow)
