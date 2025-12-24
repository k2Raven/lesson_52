from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
        print(self.request.user)
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

@method_decorator(ensure_csrf_cookie, name='dispatch')
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


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm
    model = Article
    permission_required = 'webapp.change_article'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    # def get_success_url(self):
    #     return reverse('webapp:article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'article/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:article_list')
    permission_required = 'webapp.delete_article'


class TestView(View):
    def get(self, request, pk, *args, **kwargs):
        print(pk)
        print(request.user)
        return JsonResponse({'pk': pk, 'test': 'text', 'number': 123})

    def post(self, request, pk, *args, **kwargs):
        print(pk)
        print(request.user)
        print(request.body)
        return JsonResponse({'pk': pk, 'test': 'text', 'number': 123})

