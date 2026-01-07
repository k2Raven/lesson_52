from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v3.premissions import IsAuthorOrReadOnly
from webapp.models import Article, Comment
from api_v3.serializers import ArticleSerializer, CommentSerializer, ArticleListSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Article.objects.all()
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        print(self.request.user)
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    @action(detail=True, methods=['GET'], url_path='comments')
    def get_comments(self, request, *args, **kwargs):
        print(request)
        print(request.data)
        article = self.get_object()
        return Response(CommentSerializer(article.comments.all(), many=True).data)

    @action(detail=False, methods=['GET'], url_path='count')
    def get_articles_count(self, request, *args, **kwargs):
        return Response({'count': Article.objects.count()})


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})
