from django.contrib import admin
from .models import Article, Comment
from django.db import models
from django.forms import TextInput, Textarea

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'name', 'article', 'created', 'showing')

class CommentsInline(admin.TabularInline):
    model = Comment
    extra  = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), 'seo_title' : ('title',), }
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'180'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':240})},
    }
    fieldsets = (
        ('Article', {
            'fields': ('title', 'text', 'image', 'tags', 'urlimage')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'slug')
        }),
        ('Advanced options', {
            'fields': ('user', 'published', 'status'),
        }),
    )
    list_display = ('title', 'status', 'slug', 'user')
    list_filter = ('status', 'user')
    search_fields = ('title', 'text', 'seo_description')
    actions = ['publish', 'unpublish', 'unpublish_to_draft']
    inlines = [CommentsInline]

    def publish(self, request, queryset):
        row_update = queryset.update(status = 'p')
        message_str = f'{row_update} rows updated'
        self.message_user(request, message_str)

    def unpublish_to_draft(self, request, queryset):
        row_update = queryset.update(status = 'd')
        message_str = f'{row_update} rows updated'
        self.message_user(request, message_str)

    def unpublish(self, request, queryset):
        row_update = queryset.update(status = 'r')
        message_str = f'{row_update} rows updated'
        self.message_user(request, message_str)