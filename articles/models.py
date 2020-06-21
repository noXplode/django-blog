from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Article(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200 )
    seo_title = models.CharField(max_length=200)
    seo_description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    tags = TaggableManager()
    

    STATUS = (
        ('d', 'Draft'),
        ('r', 'Ready to publish'),
        ('p', 'Published'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='d',
        help_text='Article status',
    )

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:viewpost', args=[self.slug])