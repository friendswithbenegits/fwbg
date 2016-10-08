# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.pm = []
        if self.user.is_authenticated():
            self.pm = self.user.get_suggestions()
            # unseen match
            matches = self.user.get_unseen_matches()
            # if any matches redirect to other
            if matches.get('status') != 400:
                # redirect to match retail
                match_id = matches.get('matches')[0].id
                return redirect(reverse("users:match-detail",
                                        args=(match_id,)))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['pm'] = self.pm
        return context
