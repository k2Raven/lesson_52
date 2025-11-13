from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, FormView

from webapp.models import Article
from webapp.forms import ArticleForm


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        context = {
            'articles': articles
        }
        return render(request, 'article_list.html', context)


class ArticleDetailView(TemplateView):
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return context


class ArticleCreateView(FormView):
    template_name = 'article_create.html'
    form_class = ArticleForm
    # success_url = reverse_lazy('article_list')

    # def get_success_url(self):
    #     return reverse('article_detail', kwargs={'pk': self.article.pk})

    def form_valid(self, form):
        self.article = Article()
        self.article.title = form.cleaned_data.get('title')
        self.article.content = form.cleaned_data.get('content')
        self.article.author = form.cleaned_data.get('author')
        self.article.save()
        self.article.tags.set(form.cleaned_data.get('tags'))
        return redirect('article_detail', pk=self.article.pk)

        # return super().form_valid(form)

def article_update_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(initial={'title': article.title, 'content': article.content, 'author': article.author,
                                    'tags': article.tags.all()})
        return render(request, 'article_update.html', {'form': form})
    elif request.method == "POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.author = form.cleaned_data.get('author')
            article.save()
            article.tags.set(form.cleaned_data.get('tags'))
            return redirect('article_detail', pk=article.id)
        return render(request, 'article_update.html', {'form': form})


def article_delete_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article_delete.html', {'article': article})
    article.delete()
    return redirect('article_list')
