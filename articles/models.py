from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Article(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    seo_title = models.CharField(max_length=200)
    seo_description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True)
    tags = TaggableManager(blank=True)
    urlimage = models.URLField(blank=True, null=True)

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

    def get_similar_posts(self):
        return self.tags.similar_objects()[:3]  # inherited from taggit

    def get_nonparent_comments(self):
        return self.comment_set.filter(parent__isnull=True)  # non replies comments


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    showing = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.text
