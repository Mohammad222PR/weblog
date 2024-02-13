from account.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    ##################
    # Custom Manager.#
    #################


# class ArticleManger(models.Manager):
#     def get_queryset(self):
#         return super(ArticleManger, self).get_queryset().filter(is_published = True)

class Article(models.Model):
    STATUS = [
        ("Publish", "Publish"),
        ("Unpublished", "Unpublished"),
        ("Draft", "Draft")
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    tag = models.ManyToManyField(Tag, related_name='articles')
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=100000)
    image = models.ImageField(upload_to='images/articles')
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    updated = models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(User, default=None, blank=True, null=True, related_name='favorite')
    status = models.CharField(max_length=20, choices=STATUS, default="Draft")

    # custom_manager = ArticleManger()

    def __str__(self):
        return self.title

    def image_tag(self):
        return format_html("<img src='{}' width=100 height=100 style='border-radius: 10px;'>".format(self.image.url))

    image_tag.short_description = 'image'

    ###########################################################################################
    # Save method : if title send database this method run and create new tag from title name.#
    ###########################################################################################

    class Meta:
        ordering = ('-created',)
    # def save(self, *args, **kwargs):
    #     if self.title:
    #         super(Article, self).save(args, kwargs)
    #         Tag.objects.create(title=self.title)
    #


# Class Comment.
class Comment(models.Model):
    articles = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    body = models.TextField(max_length=1000)
    created_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


# Contact Form.
class Contact(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    number = models.IntegerField(verbose_name='Enter your number', null=True, blank=True)
    subject = models.CharField(max_length=1000)
    message = models.TextField(max_length=1000000)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
