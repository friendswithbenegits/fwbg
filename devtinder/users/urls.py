# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(regex=r'^$', view=views.UserListView.as_view(), name='list'),
    url(regex=r'^~redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
    url(regex=r'^~update/$', view=views.UserUpdateView.as_view(), name='update'),
    # user actions
    url(regex=r'^action/(?P<action>[a-zA-Z0-9-]+)/(?P<to_user>[a-zA-Z0-9-+_.]+)$', view=views.UserActionView.as_view(), name='action'),
    url(regex=r'^(?P<username>[\w.@+-]+)/add-snippet/$', view=views.UserSelectSnippetView.as_view(), name='add-snippet'),
]
