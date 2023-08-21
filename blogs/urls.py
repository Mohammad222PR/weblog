from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('detail/<slug:slug>', views.PostDetailView.as_view(), name='blog_detail'),
    path('list',views.PostListView.as_view(), name='blog_list'),
    path('category/<int:pk>', views.category_detail.as_view(), name='cat_list'),
    path('tag/<int:pk>', views.tag_detail.as_view(), name='tag_list'),

]