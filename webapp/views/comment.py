from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse

from webapp.forms import CommentForm
from webapp.models import Article, Comment


class CommentCreateView(UserPassesTestMixin, CreateView):
    template_name = 'comment/comment_create.html'
    form_class = CommentForm

    def test_func(self):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return self.request.user.is_authenticated and article.author != self.request.user

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.article.pk})

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        form.instance.article = article
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'comment/comment_update.html'
    form_class = CommentForm
    model = Comment
    permission_required = 'webapp.change_comment'

    def has_permission(self):
        return super().has_permission() and self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.article.pk})

class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = 'webapp.delete_comment'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:article_detail', kwargs={'pk': self.object.article.pk})