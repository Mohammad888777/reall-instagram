from django.db import models
from accounts.models import User
from posts.models import Post
from comments.models import Comment

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'),(4,"Direct"),(5,'replay_comment'),(6,"likeComment"))

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="notification_post", null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="notification_comment", null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_sender" )
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_receiver" )
    notification_types = models.IntegerField(choices=NOTIFICATION_TYPES, null=True, blank=True)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username



