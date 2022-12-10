from django.db import models
from accounts.models import User
from posts.models import Post,Follow
from django.core.validators import FileExtensionValidator
from django.utils.html import format_html



class Profile(models.Model):

    PROFILE_STATUS=(
        ("public","public"),
        ("private","private"),
    )
    # REQUEST_STATUS=(

    #     ("empty","empty"),
    #     ("requested","requested"),
    #     ("accepted","accepted"),
    #     ("rejected","rejected"),
    # )

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(upload_to="profile_pciture", null=True, default="default.jpg",validators=[FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])])
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    favourite = models.ManyToManyField(Post, blank=True)
    status=models.CharField(max_length=200,null=True,choices=PROFILE_STATUS,default="public")
    # request_status=models.CharField(max_length=200,null=True,choices=REQUEST_STATUS,default="empty")

    follwer_requested = models.ManyToManyField(Follow, blank=True,related_name="requests")

    def __str__(self) -> str:
        return  self.user.username
    
    def image_profile(self):

        if self.image:
            return format_html(f"<img src='{self.image.url}' width='50px' height='50px'  ")
        return "alt"
        

