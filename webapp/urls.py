from django.urls import path
from webapp.views import article_list_view

urlpatterns = [
    path('', article_list_view),
]
