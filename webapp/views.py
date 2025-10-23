from django.shortcuts import render

from webapp.models import Article


def article_list_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'article_list.html', context)
