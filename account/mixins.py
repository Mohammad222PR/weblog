from django.http import Http404
from django.shortcuts import get_object_or_404

from blogs.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['category', 'tag', 'title', 'body', 'image', 'slug', 'is_special','status']

        if request.user.is_superuser:
            self.fields.append('author')

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
            if self.obj.status != 'I':
                self.obj.status = 'Draft'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['Draft', 'b'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page")


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("You can't see this page")
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
