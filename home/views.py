from django.shortcuts import render
from django.views import View
from blogs.models import *
# Create your views here.


class HomeView(View):
    def get(self, request):
        articles = Article.objects.all()
        return render(request, 'home/index.html', {'articles': articles})

