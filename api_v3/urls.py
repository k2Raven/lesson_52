from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api_v3.views import ArticleViewSet, CommentsViewSet, LogoutView

router = routers.DefaultRouter()
router.register('articles', ArticleViewSet)
router.register('comments', CommentsViewSet)
# router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
]
