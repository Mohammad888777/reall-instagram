# from django.db import models
# from accounts.models import User
# from posts.models import Post
# from comments.models import Comment
# from profiles.models import Profile



# class Story(models.Model):

#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     seener=models.ManyToManyField(User,related_name="user_seener")
#     image_or_viedo=models.FileField()
#     # created
#     # updated
#     is_seen=models.BooleanField(default=False)
#     text_box=models.TextField()
