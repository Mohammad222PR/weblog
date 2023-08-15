from django.contrib.auth.models import User
from django.db import models
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    tag = models.ManyToManyField(Tag, related_name='tags')
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=100000)
    image = models.ImageField(upload_to='images/articles')
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    # custom_manager = ArticleManger()

    def __str__(self):
        return f"{self.title} -- {self.body} -- {self.image} -- {self.is_published}"

        ###########################################################################################
        # Save method : if title send database this method run and create new tag from title name.#
        ###########################################################################################

    # def save(self, *args, **kwargs):
    #     if self.title:
    #         super(Article, self).save(args, kwargs)
    #         Tag.objects.create(title=self.title)
    #

