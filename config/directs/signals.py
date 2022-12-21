from django.db.models.signals import post_delete,post_save
from .models import Thread,Message
from notifications.models import Notification


def receive_message_signal(sender,created,instance,**kwargs):

    if created:
        Notification.objects.create(
            sender=instance.sender_user,receiver=instance.receiver_user,
            notification_types=4,
        )


def delete_message_signal(sender,instance,**kwargs):

        n=Notification.objects.create(
            sender=instance.sender_user,receiver=instance.receiver_user,
            notification_types=4,
        )
        n.delete()
    

post_save.connect(receive_message_signal,sender=Message)
post_delete.connect(delete_message_signal,sender=Message)


