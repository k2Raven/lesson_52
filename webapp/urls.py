from django.urls import path
from webapp.views import article_list_view, article_detail_view, article_create_view, article_update_view, \
    article_delete_view

urlpatterns = [
    path('', article_list_view, name='article_list'),
    path('article/<int:pk>/', article_detail_view, name='article_detail'),
    path('article/create/', article_create_view, name='article_create'),
    path('article/<int:pk>/update/', article_update_view, name='article_update'),
    path('article/<int:pk>/delete/', article_delete_view, name='article_delete')

]
