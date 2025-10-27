from django.urls import path
from webapp.views import article_list_view, article_detail_view, article_create_view

urlpatterns = [
    path('', article_list_view, name='article_list'),
    path('article/<int:pk>/', article_detail_view, name='article_detail'),
    path('article/create/', article_create_view, name='article_create'),
]
