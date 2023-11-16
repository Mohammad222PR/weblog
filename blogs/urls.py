from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('detail/<slug:slug>', views.PostDetailView.as_view(), name='blog_detail'),
    path('list',views.PostListView.as_view(), name='blog_list'),
    path('category/<int:pk>', views.category_detail.as_view(), name='cat_list'),
    path('tag/<int:pk>', views.tag_detail.as_view(), name='tag_list'),
    path('comment/delete/<int:pk>/<slug:slug>', views.DeleteCommentView.as_view(), name='comment_delete'),
    path('search', views.SearchView.as_view(), name='search'),
    path('contact', views.ContactsView.as_view(), name='contact'),
    path('like/<slug:slug>/<int:pk>', views.LikeView.as_view(), name='like_article'),
    path('favorite/<int:id>', views.FavoriteView.as_view(), name='favorite_article'),
    path('favorite/list', views.FaveView.as_view(), name='favorite_list')

]