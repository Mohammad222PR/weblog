from django.contrib import admin
from django.db.models import Q

from .models import *


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'created', 'category', 'status')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['image_tag']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True) | Q(is_author=True))
            return super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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
    list_display = ('user', 'name', 'email', 'subject', 'message', 'created')
    search_fields = ('name', 'email', 'subject', 'message', 'created')
    list_filter = ('created',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'user')


@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)


admin.site.register(ArticleHint)
