from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, reverse, redirect

from webapp.models import Article


def article_list_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'article_list.html', context)

def article_detail_view(request, *args, pk, **kwargs):
    # try:
    #     article = Article.objects.get(id=pk)
    #     return render(request, 'article_detail.html', {'article': article})
    # except Article.DoesNotExist:
    #     # return HttpResponseNotFound('<h1>Article not found</h1>')
    #     raise Http404()
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
        # return render(request, 'article_create.html', {'status_choices': status_choices})
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        article = Article.objects.create(title=title, content=content, author=author)
        # return HttpResponseRedirect(reverse('article_list'))
        # return redirect('article_list')
        return redirect('article_detail', pk=article.id)