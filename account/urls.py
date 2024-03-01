from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, re_path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
    path('register/', views.Register.as_view(), name='user_register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    path('home/', views.AccountHomeView.as_view(), name='home'),
    path('profile/edit/', views.profile_normal_user_view, name='profile-edit'),
    path('search/', views.article_search, name='search'),
    path('article/create', views.ArticleCreateView.as_view(), name='article-create'),
    path('article/update/<int:pk>', views.ArticleUpdateView.as_view(), name='article-update'),
    path('article/delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('profile', views.ProfileUpdateView.as_view(), name='profile'),

]
