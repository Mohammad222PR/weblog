from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
    path('register/', views.register, name='user_register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_normal_user_view, name='profile-edit'),
    path('search/', views.article_search, name='search'),
    path('article/create', views.ArticleCreateView.as_view(), name='article-create')

]
