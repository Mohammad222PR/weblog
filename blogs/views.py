from django.shortcuts import render, get_object_or_404
from django.views import View
from blogs.models import Article, Tag, Category


# Create your views here


class PostDetail(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        categories = Category.objects.all()
        articles = Article.objects.filter(is_published=True).order_by("-created",)[:5]
        return render(request, 'blogs/article_detail.html', {'article':article,'articles':articles, 'categories':categories})
