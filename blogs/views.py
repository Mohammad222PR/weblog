from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from blogs.models import Article, Category, Tag


# Create your views here


class PostDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        categories = Category.objects.all()
        resent_article = Article.objects.filter(is_published=True).order_by("-updated")[:3]
        return render(request, 'blogs/article_detail.html',
                      {'article': article, 'resent_article': resent_article, 'categories': categories})


class PostListView(View):
    def get(self, request):
        articles = Article.objects.filter(is_published=True)
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article-list.html', {'articles': objects_list})


class category_detail(View):
    def get(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        articles = category.categories.all()
        return render(request, "blogs/article-list.html", {'articles': articles})


class tag_detail(View):
    def get(self, request, pk=None):
        tag = get_object_or_404(Tag, id=pk)
        articles = tag.tags.all()
        return render(request, "blogs/article-list.html", {'articles': articles})
