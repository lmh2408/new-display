from django.db import models

# Create your models here.
class Section(models.Model):
    section = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(default=0)

class Article(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100, unique=False, default='Anonymous')
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    header = models.CharField(max_length=200, unique=False)
    subheader = models.CharField(max_length=400, unique=False)
    thumbnail = models.ImageField(upload_to='image/thumbnail/', blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-last_updated']


class FrontPage(models.Model):
    prominent = models.BooleanField(default=False)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(upload_to='image/')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, blank=True, null=True)
