from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from account.models import User
from django.urls import reverse_lazy

from account.forms import LoginForm, SingupForm, EditAccountForm
from blogs.models import Article
from django.views import generic


# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                auth_login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('account:profile')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['password1'], cd['password2'])
            user = authenticate(request, username=cd['username'], password=cd['password1'])
            auth_login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home:home')

    else:
        form = SingupForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)

    return redirect('home:home')


@login_required
def profile_view(request):
    user = request.user
    form = EditAccountForm(instance=user)
    if request.method == 'GET':
        if request.user.is_authenticated:
            if user.is_superuser:
                articles = Article.objects.all().order_by('-created')
            elif user.is_author:
                articles = Article.objects.filter(author=request.user).order_by('-created')
            else:
                return redirect('account:profile-edit', user.id)
        return render(request, 'account/index.html', {'form': form, 'articles': articles})


@login_required()
def article_search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        articles = Article.objects.filter(title__icontains=q)
        return render(request, 'account/index.html', {'articles': articles, 'q': q})


@login_required
def profile_normal_user_view(request):
    user = request.user
    form = EditAccountForm(instance=user)

    if request.method == 'POST':
        form = EditAccountForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:profile-edit')
    return render(request, 'account/edit_account.html', {'form': form})


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    fields = '__all__'
    template_name = 'account/article-create-update.html'
    success_url = reverse_lazy('account:profile')
