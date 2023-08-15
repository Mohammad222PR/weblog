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