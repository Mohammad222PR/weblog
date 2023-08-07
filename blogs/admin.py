from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')

@admin.register(Tag)
class CustomTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')