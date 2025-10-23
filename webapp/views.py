from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.models import Article


def article_list_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'article_list.html', context)

def article_detail_view(request):
    article_id = request.GET.get('id')
    if article_id:
        article = Article.objects.get(id=article_id)
        return render(request, 'article_detail.html', {'article': article})
    else:
        return HttpResponseRedirect('/')
