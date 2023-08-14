from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('detail/<int:pk>/',views.PostDetail.as_view(), name='blog_detail'),
]