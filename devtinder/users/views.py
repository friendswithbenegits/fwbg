# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import (DetailView, ListView, RedirectView,
                                  UpdateView, View)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User

import logging
logger = logging.getLogger(__name__)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
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
        to_user = kwargs.get('to_user')
        logger.info("User {} {} user {}.".format(from_user, action, to_user))
        return redirect(reverse('home'))