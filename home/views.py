from django.shortcuts import render
from django.views import View
from blogs.models import *
from blogs.views import PostDetailView


# Create your views here.


class HomeView(View):
    def get(self, request):
        articles = Article.objects.filter(is_published=True).order_by("-created", )[:5]
        tags = Tag.objects.prefetch_related('articles').all()
        categories = Category.objects.prefetch_related('articles').all()
        return render(request, 'home/index.html', {'articles': articles, 'tags': tags, 'categories': categories})
