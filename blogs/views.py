from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import ListView, FormView, CreateView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.forms import ContactForm, CommentForm
from blogs.models import Article, Category, Tag, Comment, Contact, Like


# Create your views here


class PostDetailView(View):
    form_class = CommentForm

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        categories = Category.objects.all()
        resent_article = Article.objects.filter(is_published=True).order_by("-updated")[:3]
        if request.user.is_authenticated:

            if request.user.likes.filter(article__slug=slug, user_id=request.user.id).exists():
                is_likes = True
            else:
                is_likes = False

            if article.favorite.filter(id=request.user.id).exists():
                is_fave = True
            else:
                is_fave = False


            return render(request, 'blogs/article_detail.html',
                          {'article': article, 'resent_article': resent_article, 'categories': categories,
                           'is_likes': is_likes, 'is_fave': is_fave})
        else:
            return render(request, 'blogs/article_detail.html',
                          {'article': article, 'resent_article': resent_article, 'categories': categories})

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        comment = Comment.objects.create(body=body, articles=article, user=request.user, parent_id=parent_id)
        comment.save()
        messages.success(request, 'Youre comment is added successfully', 'success')
        return redirect('blog:blog_detail', article.slug)


class DeleteCommentView(View):
    def get(self, request, pk, slug):
        article = get_object_or_404(Article, slug=slug)
        comment = get_object_or_404(Comment, id=pk)
        if comment.user.id == request.user.id:
            comment.delete()
            messages.success(request, 'Youre comment is delete', 'warning')
            return redirect('blog:blog_detail', article.slug)


class PostListView(View):
    def get(self, request):
        articles = Article.objects.filter(is_published=True)
        tags = Tag.objects.all()
        categories = Category.objects.all()
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article_list.html',
                      {'articles': objects_list, 'tags': tags,
                       'categories': categories})


# class PostListView(ListView):
#     model = Article
#     paginate_by = 1
#     context_object_name = 'articles'
#     queryset = Article.objects.filter(is_published=True)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PostListView)

class category_detail(View):
    def get(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        articles = category.categories.all()
        tags = Tag.objects.all()
        categories = Category.objects.all()
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, "blogs/article_list.html",
                      {'articles': objects_list, 'category': category, 'tags': tags, 'categories': categories})


class tag_detail(View):
    def get(self, request, pk=None):
        tag = get_object_or_404(Tag, id=pk)
        articles = tag.articles.all()
        tags = Tag.objects.all()
        categories = Category.objects.all()
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article_list.html',
                      {'articles': objects_list, 'tag': tag, 'tags': tags, 'categories': categories})


class SearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        articles = Article.objects.filter(title__icontains=q)
        tags = Tag.objects.all()
        categories = Category.objects.all()
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article_list.html',
                      {'articles': objects_list, 'q': q, 'tags': tags, 'categories': categories})


# class ContactsView(View):
#     form_class = ContactForm
#
#     def get(self, request):
#         return render(request, 'blogs/contact.html')
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             new = form.save(commit=False)
#             new.user = request.user
#             new.save()
#             messages.success(request, 'Youre contact is sucess', 'success')
#             return redirect('blog:contact')
#         return render(request, 'blogs/contact.html')
#

class ContactsView(CreateView):
    template_name = 'blogs/contact.html'
    model = Contact
    fields = "__all__"
    success_url = reverse_lazy('blog:contact')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class LikeView(LoginRequiredMixin, View):
    def get(self, request, slug, pk):
        try:
            like = Like.objects.get(article__slug=slug, user_id=request.user.id)
            like.delete()
            return JsonResponse({'response': 'dislike'})
        except:
            Like.objects.create(article_id=pk, user_id=request.user.id)
            return JsonResponse({'response': 'like'})


class FavoriteView(LoginRequiredMixin, View):
    def get(self, request, slug):
        blog = Article.objects.get(slug=slug)

        if blog.favorite.remove(id=request.user.id).exists():
            blog.favorite.delete(request.user)
            return JsonResponse({'response': 'deleted'})
        else:
            blog.favorite.add(request.user)
            return JsonResponse({'response': 'added'})


class FaveView(View):
    def get(self, request, slug, pk):
        blog = Article.objects.all(slug=slug)

        if blog == request.user.id:
            fave = blog.favorite.all(request.user)
        return render(request, 'blogs/favoirte.html', {'favoirte': fave})
