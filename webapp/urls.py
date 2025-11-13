from django.urls import path
from webapp.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, \
    article_delete_view

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', article_delete_view, name='article_delete')

]
