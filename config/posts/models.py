from django.db import models
import uuid
from django.utils.text import slugify
from accounts.models import User

from django.db.models.signals import post_save, post_delete



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    



class Post(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name="Picture")
    caption = models.CharField(max_length=10000, verbose_name="Caption")
    posted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    # def get_absolute_url(self):
    #     return reverse("post-details", args=[str(self.id)])

    def __str__(self):
        return str(self.caption)





class Like(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_likes")



    def __str__(self) -> str:
        return self.user.username


class Follow(models.Model):
    REQUEST_STATUS=(

        ("empty","empty"),
        ("requested","requested"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    )

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    request_status=models.CharField(max_length=200,null=True,choices=REQUEST_STATUS,default="empty")






class Stream(models.Model):
    
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following') #sender
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #receiver
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        profile=user.profile
        followers=None
        
        
       
        if profile.status=="private":
            followers = Follow.objects.all().filter(following=user,request_status="accepted")



        if profile.status=="public":
            followers = Follow.objects.all().filter(following=user,request_status="empty")

        for follower in followers:
            stream = Stream.objects.get_or_create(post=post, user=follower.follower, date=post.posted, following=user)
    
    

    def auto_delete_stream(sender,instance,**kwargs):
        s=Stream.objects.filter(

            following=instance.following,

        )
        s.delete()



post_save.connect(Stream.add_post, sender=Post)
post_delete.connect(Stream.auto_delete_stream,sender=Follow)