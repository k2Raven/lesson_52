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
        return render(request, 'article/article_list.html', context)


class ArticleDetailView(TemplateView):
    template_name = 'article/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return context


class ArticleCreateView(FormView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        self.article = form.save()
        return redirect('article_detail', pk=self.article.pk)



class ArticleUpdateView(FormView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.article.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)





def article_delete_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article/article_delete.html', {'article': article})
    article.delete()
    return redirect('article_list')
