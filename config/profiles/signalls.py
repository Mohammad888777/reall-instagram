from django.db.models.signals import post_delete,post_save
from .models import Profile
from accounts.models import User

def auto_create_profile(sender,created,instance,**kwargs):

    if created:
        Profile.objects.create(
            user=instance
        )


def auto_delete_profile(sender,instance,**kwargs):

    pass

post_save.connect(auto_create_profile,sender=User)