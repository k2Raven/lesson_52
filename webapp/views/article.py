from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView, FormView, ListView, DetailView

from webapp.models import Article
from webapp.forms import ArticleForm, SimpleSearchForm


class ArticleListView(ListView):
    template_name = 'article/article_list.html'
    model = Article
    context_object_name = 'articles'
    paginate_by = 4

    def dispatch(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) |
                                       Q(content__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search_value'] = self.search_value
        return context

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        search_value = ''
        if self.search_form.is_valid():
            search_value = self.search_form.cleaned_data.get('search', '')
        return search_value


class ArticleDetailView(DetailView):
    template_name = 'article/article_detail.html'
    model = Article
    # pk_url_kwarg = 'pk'
    # context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['comments'] = article.comments.order_by('-created_at')
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
