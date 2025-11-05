from django.shortcuts import render, get_object_or_404, redirect

from webapp.models import Article
from webapp.forms import ArticleForm


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
        form = ArticleForm()
        return render(request, 'article_create.html', {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('article_detail', pk=article.id)

        return render(request, 'article_create.html', {'form': form})


def article_update_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(instance=article)
        return render(request, 'article_update.html', {'form': form})
    elif request.method == "POST":
        form = ArticleForm(data=request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('article_detail', pk=article.id)
        return render(request, 'article_update.html', {'form': form})




def article_delete_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article_delete.html', {'article': article})
    article.delete()
    return redirect('article_list')
