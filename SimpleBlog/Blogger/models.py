from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('view_post', args=[str(self.id)])

class Comment(models.Model):
    creator = models.CharField(max_length=200)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    post = models.ForeignKey(Post)

