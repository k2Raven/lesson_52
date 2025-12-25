from django.urls import path

from api_v2.views import get_token_view, ArticleView

urlpatterns = [
    path('get_token/', get_token_view),
    path('article/', ArticleView.as_view()),
    path('article/<int:pk>/', ArticleView.as_view()),
]