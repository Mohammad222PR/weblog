from django.shortcuts import render, get_object_or_404
from django.views import View

from blogs.models import Article, Category, Tag


# Create your views here


class PostDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        categories = Category.objects.all()
        articles = Article.objects.filter(is_published=True).order_by("-updated")[:3]
        return render(request, 'blogs/article_detail.html', {'article':article,'articles':articles, 'categories':categories})


class PostListView(View):
    def get(self, request):
        articles = Article.objects.filter(is_published=True)
        resent_article = Article.objects.all().order_by("-updated",)[:3]
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(request, 'blogs/article-list.html', {'articles':articles,'tags':tags,'categories':categories ,'resent_article':resent_article})
