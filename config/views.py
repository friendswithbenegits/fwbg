# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            # unseen match
            context['matches'] = user.get_unseen_matches()
            # suggestions
            context['pm'] = user.get_suggestions()
        return context
