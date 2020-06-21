from django.contrib import admin
from .models import Article
from django.db import models
from django.forms import TextInput, Textarea

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), 'seo_title' : ('title',), }
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'180'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':240})},
    }
    fieldsets = (
        ('Article', {
            'fields': ('title', 'text', 'image', 'tags')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'slug')
        }),
        ('Advanced options', {
            'fields': ('user', 'published', 'status'),
        }),
    )
    list_display = ('title', 'status', 'slug', 'user', 'published')