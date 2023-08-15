from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('detail/<slug:slug>/',views.PostDetail.as_view(), name='blog_detail'),
    path('list/', views.PostListView.as_view(), name='blog_list'),
]