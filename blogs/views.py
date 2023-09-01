from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from blogs.forms import ContactForm, CommentForm
from blogs.models import Article, Category, Tag, Comment, Contact


# Create your views here


class PostDetailView(View):
    form_class = CommentForm

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        categories = Category.objects.all()
        resent_article = Article.objects.filter(is_published=True).order_by("-updated")[:3]
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
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article-list.html', {'articles': objects_list})


class category_detail(View):
    def get(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        articles = category.categories.all()
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, "blogs/article-list.html", {'articles': objects_list, 'category': category})


class tag_detail(View):
    def get(self, request, pk=None):
        tag = get_object_or_404(Tag, id=pk)
        articles = tag.tags.all()
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article-list.html', {'articles': objects_list, 'tag': tag})


class SearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        articles = Article.objects.filter(title__icontains=q)
        page_number = request.GET.get('page')
        paginator = Paginator(articles, 1)
        objects_list = paginator.get_page(page_number)

        return render(request, 'blogs/article-list.html', {'articles': objects_list, 'q': q})


# View for Contacts.
class ContactsView(View):
    form_class = ContactForm

    def get(self, request):
        return render(request, 'blogs/contact.html')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            messages.success(request, 'Youre contact is sucess', 'success')
            return redirect('blog:contact')
        return render(request, 'blogs/contact.html')
