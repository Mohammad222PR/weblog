from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'category')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class CustomTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('articles', 'user', 'parent', 'body', 'created_add')
    search_fields = ('article', 'user', 'parent', 'body', 'created_add')
    list_filter = ('created_add',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'created')
    search_fields = ('name', 'email', 'subject', 'message', 'created')
    list_filter = ('created',)
