from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import *
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import CreateView

from account.mixins import (
    FieldsMixin,
    FormValidMixin,
    AuthorAccessMixin,
    ArticleDeleteMixin,
    ProfileMixin, AuthorsAccessMixin,
)
from account.models import User
from django.urls import reverse_lazy

from account.forms import LoginForm, SignupForm, EditAccountForm, ProfileForm
from blogs.models import Article
from django.views import generic, View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                auth_login(request, user)
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect("account:home")

    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


class Register(CreateView):
    form_class = SignupForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('account/email/registration/acc_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),

            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال‌سازی به ایمیل شما ارسال شد. <a href="account/login/" >ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('اکانت شما با موفقیت فعال شد.')
    else:
        return HttpResponse('ادرس فعال سازی معتبر نیست!')


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        next_page = request.GET.get("next")
        if next_page:
            return redirect(next_page)

        return redirect("home:home")


class AccountHomeView(LoginRequiredMixin, AuthorsAccessMixin, View):
    def get(self, request):
        user = request.user
        form = EditAccountForm(instance=user)
        if request.user.is_authenticated:
            if user.is_superuser:
                articles = Article.objects.all().order_by("-created")
            elif user.is_author or user.is_staff:
                articles = Article.objects.filter(author=request.user).order_by(
                    "-created"
                )
            else:
                return redirect("account:profile-edit")
        return render(
            request, "account/index.html", {"form": form, "articles": articles}
        )


@login_required()
def article_search(request):
    if request.method == "GET":
        q = request.GET.get("q")
        articles = Article.objects.filter(title__icontains=q)
        return render(request, "account/index.html", {"articles": articles, "q": q})


@login_required
def profile_normal_user_view(request):
    user = request.user
    form = EditAccountForm(instance=user)

    if request.method == "POST":
        form = EditAccountForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("account:profile-edit")
    return render(request, "account/edit_account.html", {"form": form})


class ArticleCreateView(
    FieldsMixin, LoginRequiredMixin, FormValidMixin, generic.CreateView
):
    model = Article
    fields = "__all__"
    template_name = "account/article-create-update.html"
    success_url = reverse_lazy("account:home")


class ArticleUpdateView(
    FieldsMixin,
    LoginRequiredMixin,
    AuthorAccessMixin,
    FormValidMixin,
    generic.UpdateView,
):
    model = Article
    fields = "__all__"
    template_name = "account/article-create-update.html"
    success_url = reverse_lazy("account:home")


class ProfileUpdateView(LoginRequiredMixin, ProfileMixin, generic.UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_url = reverse_lazy("account:home")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class ArticleDeleteView(LoginRequiredMixin, ArticleDeleteMixin, generic.DeleteView):
    model = Article
    template_name = "account/article_confirm_delete.html"
    success_url = reverse_lazy("account:home")

# class PasswordResetForm(PasswordResetForm):
#     template_name = "account/password_reset_form.html"
#     success_url = reverse_lazy("account:passowrd_reset_done")
#
# class PasswordResetConfrim(PasswordResetConfirmView):
#     template_name = 'account/password_reset_confrim.html'
#     success_url = reverse_lazy("account:password_reset_complete")
