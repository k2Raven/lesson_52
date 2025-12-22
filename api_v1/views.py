import json
from datetime import datetime
from http import HTTPStatus

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class JsonEchoView(View):
    def get(self, request, *args, **kwargs):
        answer = {
            'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
            'method': 'GET'
        }
        if request.body:
            answer['body'] = json.loads(request.body)
        return JsonResponse(answer)

    def post(self, request, *args, **kwargs):
        answer = {
            'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
            'method': 'POST'
        }
        if request.body:
            answer['body'] = json.loads(request.body)
        return JsonResponse(answer, status=HTTPStatus.OK)

class ArticleView(View):
    def get(self, request, *args, **kwargs):
        # articles = Article.objects.values('id', 'title', 'author__username')
        articles = Article.objects.all()
        articles = serialize('json', articles)
        # return JsonResponse(articles, safe=False)
        return HttpResponse(articles, content_type='application/json')