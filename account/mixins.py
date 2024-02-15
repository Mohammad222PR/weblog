from django.http import Http404
from django.shortcuts import get_object_or_404

from blogs.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = "__all__"
        elif request.user.is_author:
            self.fields = ['category', 'tag', 'title', 'body', 'image', 'slug', 'is_special']
        else:
            raise Http404("You can't see this page")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = "Draft"
        return super().form_valid(form)


class ArticleAccessMixin():
    def dispatch(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['Draft', 'b'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page")


class ArticleDeleteMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't delete this post")


class ProfileMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_author or request.user.is_staff:
            return super().dipatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page")
