from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse

from webapp.forms import CommentForm
from webapp.models import Article, Comment


class CommentCreateView(CreateView):
    template_name = 'comment/comment_create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        form.instance.article = article
        return super().form_valid(form)

class CommentUpdateView(UpdateView):
    template_name = 'comment/comment_update.html'
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})