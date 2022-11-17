from django.db import models
from django.contrib.auth import get_user_model
from .initials import Initials

User = get_user_model()
    
class Feed(Initials):
    author = models.OneToOneField(User,on_delete=models.CASCADE, related_name='feed_author')
    slug = models.SlugField(blank=True)
    
    # post = models.ForeignKey()
    def __str__(self):
        return self.author.username
        
class Post(Initials):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_author')
    feed = models.ForeignKey(Feed,on_delete=models.PROTECT,related_name='feed_post')

    def __str__(self):
        return f"Posted by {self.author.username}."

    
class Comment(Initials):
    post = models.ForeignKey(Post, related_name="comments_post", on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_user')
    
    def __str__(self):
        return self.content

class Like(Initials):
    liker = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Liker_user')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like_post')

    def __str__(self):
        return f"{self.liker.username} like {self.post}."
