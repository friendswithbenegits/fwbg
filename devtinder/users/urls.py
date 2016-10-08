# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(regex=r'^$', view=views.UserListView.as_view(), name='list'),
    # user actions urls
    url(regex=r'^action/(?P<action>[a-zA-Z0-9-]+)/(?P<to_user>[a-zA-Z0-9-+_.]+)$', view=views.UserActionView.as_view(), name='action'),
    url(regex=r'^snippet-action/(?P<action>[a-zA-Z0-9-]+)/(?P<snippet_id>[a-zA-Z0-9-+_.]+)$', view=views.UserSnippetActionView.as_view(), name='snippet-action'),
    # matches urls
    url(regex=r'^matches/$', view=views.UserMatchesView.as_view(), name='matches'),
    url(regex=r'^match/(?P<match_id>[a-zA-Z0-9-+_.]+)/$', view=views.UserMatchDetailView.as_view(), name='match-detail'),
    url(regex=r'^all-match-messages/(?P<match_id>[a-zA-Z0-9-+_.]+)/$', view=views.AllMatchMessages.as_view(), name='match-messages'),
    url(regex=r'^add-snippet/$', view=views.UserSelectSnippetView.as_view(), name='add-snippet'),
    url(regex=r'^~redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    url(regex=r'add-snippet/$', view=views.UserSelectSnippetView.as_view(), name='add-snippet'),
    url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
    url(regex=r'^~update/$', view=views.UserUpdateView.as_view(), name='update'),


]
