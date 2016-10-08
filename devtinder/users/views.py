# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import (DetailView, ListView, RedirectView,
                                  UpdateView, View, FormView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import User, RepositorySnippet, UserMatch
from .forms import RepoUrlInputFrom
from .services import get_data

import logging
logger = logging.getLogger(__name__)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['snippets'] = RepositorySnippet.objects.filter(owner=self.user)
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'email']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username,
                               'email': self.request.user.email})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserActionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        from_user = request.user
        action = kwargs.get('action')
        to_user = User.objects.get(username=kwargs.get('to_user'))
        print("User {} {} user {}.".format(from_user, action, to_user))

        if action == 'like':
            from_user.give_like(to_user)
        elif action == 'dislike':
            from_user.give_dislike(to_user)
        else:
            pass
        return redirect(reverse('home'))

class UserSnippetActionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        from_user = request.user
        action = kwargs.get('action')
        snippet = kwargs.get('snippet_id')
        print("User \"{}\" performed action \"{}\" on snippet \"{}\".".format(
            from_user, action, snippet))

        if action == 'delete':
            rs = RepositorySnippet.objects.filter(
                id=snippet, owner=from_user).first()
            rs.delete()
        else:
            pass
        return redirect(reverse('users:add-snippet'))


class UserSelectSnippetView(LoginRequiredMixin, FormView):
    template_name = "users/user_snippet.html"
    form_class = RepoUrlInputFrom
    success_url = "."

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        return super(UserSelectSnippetView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(UserSelectSnippetView, self).get_context_data(**kwargs)
        ctx['snippets'] = RepositorySnippet.objects.filter(owner=self.user)
        return ctx

    def form_invalid(self, form):
        return super(UserSelectSnippetView, self).form_invalid(form)

    def form_valid(self, form):
        url = form.cleaned_data['url']
        try:
            data = get_data(url, self.user)
            repository = data.get('name')
            language = data.get('language')
            stars = data.get('stars')
            snippet = data.get('snippet')
            lines = data.get('lines')
            rs = RepositorySnippet.create(self.user, repository, language,
                                          stars, snippet, lines)
            rs.save()
        except Exception, e:
            messages.add_message(self.request, messages.WARNING, e.message)
        return super(UserSelectSnippetView, self).form_valid(form)


class UserMatchesView(LoginRequiredMixin, TemplateView):
    template_name = "users/user_matches.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        return super(UserMatchesView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(UserMatchesView, self).get_context_data(**kwargs)
        ctx['matches'] = UserMatch.get_matches(self.user)
        return ctx
