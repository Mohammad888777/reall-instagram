from django.db import models
from accounts.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator


def user_directory_path(instance, filename):
    return 'Message {0}/{1}/{2}'.format(instance.sender_user.id, filename,instance.thread.id)



class Thread(models.Model):
    
    sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_sender')
    receiver=models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_receiver')
    is_seen = models.BooleanField(default=False)


class Message(models.Model):
    
    thread = models.ForeignKey(Thread, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user_messages')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user_messages')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='MessageSent', blank=True, null=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])
    video=models.FileField(upload_to='MessageSent',null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.sender_user.username