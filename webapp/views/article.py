from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Article
from webapp.forms import ArticleForm, SimpleSearchForm


class ArticleListView(ListView):
    template_name = 'article/article_list.html'
    model = Article
    context_object_name = 'articles'
    paginate_by = 4
    ordering = ['-created_at']

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

    def get_context_data(self, *, object_list=None, **kwargs):
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


class ArticleCreateView(CreateView):
    template_name = 'article/article_create.html'
    # model = Article
    # fields = ['title', 'content', 'author', 'tags']
    form_class = ArticleForm

    # def get_success_url(self):
    #     return reverse('article_detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm
    model = Article

    # def get_success_url(self):
    #     return reverse('article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    template_name = 'article/article_delete.html'
    model = Article
    success_url = reverse_lazy('article_list')
