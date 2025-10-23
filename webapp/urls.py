from django.urls import path
from webapp.views import article_list_view, article_detail_view

urlpatterns = [
    path('', article_list_view),
    path('article/', article_detail_view)
]
