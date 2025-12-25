import json

from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import get_object_or_404

from webapp.models import Article
from api_v2.serializers import  ArticleSerializer


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        serializer = ArticleSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        body = json.loads(request.body)
        serializer = ArticleSerializer(article, data=body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)
