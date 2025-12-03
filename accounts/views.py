from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm
from accounts.models import Profile

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'user_create.html'
    model = User
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get('next')
        if not next:
            next = self.request.POST.get('next')
        if not next:
            next = reverse('webapp:article_list')
        return next


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        articles = self.object.articles.order_by('-created_at')
        paginator = Paginator(articles, 4)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['articles'] = page.object_list
        kwargs['page_obj'] = page
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.get_profile_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('accounts:profile', pk=self.object.pk)
        else:
            context = self.get_context_data(form=form, profile_form=profile_form)
            return self.render_to_response(context)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'user_password_change.html'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})
