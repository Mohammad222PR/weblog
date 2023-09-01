from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.Login, name='user_login'),
    path('logout/', views.Logout, name='user_logout'),
    path('register/', views.Register, name='user_register'),
    path('edit/', views.EditAccountView, name='edit_account'),

]
