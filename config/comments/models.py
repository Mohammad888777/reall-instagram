from django.db import models
from accounts.models import User
from posts.models import Post,Tag
from django.core.validators import FileExtensionValidator



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Comment(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    body=models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to=user_directory_path,blank=True, null=True,validators=[FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])])
    # likes=models.ManyToManyField(User,related_name="comment_likes",blank=True)
    # dislikes=models.ManyToManyField(User,related_name="comment_dislikes",blank=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    tags=models.ManyToManyField(Tag,blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.body
    
    @property
    def children(self):
        return Comment.objects.select_related("user","post").prefetch_related("tags").filter(
            parent=self
        )
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        else:
            return False
    
    def create_tags(self):

        for word in self.body.split():
            if word[0]=="#":
                tag=Tag.objects.filter(title=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag=Tag(title=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                    tag.save()




class CommentLike(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="comment_likes")



    def __str__(self) -> str:
        return self.user.username