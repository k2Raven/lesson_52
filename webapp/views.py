from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.models import Article, status_choices


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


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
        # return render(request, 'article_create.html', {'status_choices': status_choices})
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        Article.objects.create(title=title, content=content, author=author)
        return HttpResponseRedirect('/')
