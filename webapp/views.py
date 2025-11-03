from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, reverse, redirect

from webapp.models import Article
from webapp.validation import validate


def article_list_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'article_list.html', context)


def article_detail_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        errors = validate(request.POST)
        article = Article()
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.author = request.POST.get('author')
        if errors:
            return render(request, 'article_create.html', {'errors': errors, 'article': article})

        article.save()
        return redirect('article_detail', pk=article.id)


def article_update_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article_update.html', {'article': article})
    elif request.method == "POST":
        article.title = request.POST.get('title')
        article.author = request.POST.get('author')
        article.content = request.POST.get('content')
        errors = validate(request.POST)
        if errors:
            return render(request, 'article_update.html', {'errors': errors, 'article': article})
        article.save()
        return redirect('article_detail', pk=article.id)


def article_delete_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article_delete.html', {'article': article})
    article.delete()
    return redirect('article_list')
