from django.urls import path

from api_v1.views import JsonEchoView, get_token_view, ArticleView

urlpatterns = [
    path('get_token/', get_token_view),
    path('echo/', JsonEchoView.as_view()),
    path('article/', ArticleView.as_view()),
]