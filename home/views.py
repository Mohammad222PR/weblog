from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.views import View
from blogs.models import *
from blogs.views import PostDetailView
from django.db.models import Count, Q


# Create your views here.


class HomeView(View):
    def get(self, request):
        articles = Article.objects.filter(status='Publish').order_by("-created", )[:5]
        last_month = datetime.today() - timedelta(days=30)
        popular_articles = Article.objects.filter(status="Publish").annotate(
            count=Count('hints', filter=Q(article_hint__created__gt=last_month))).order_by('-count', '-created')[:5]
        tags = Tag.objects.prefetch_related('articles').all()
        categories = Category.objects.prefetch_related('articles').all()
        return render(request, 'home/index.html', {'articles': articles, 'tags': tags, 'categories': categories,
                                                   'popular_articles': popular_articles})
