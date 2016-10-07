# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 10/6/16"""
__author__ = "andresilva"
__email__ = "andre@unbabel.com"
import uuid
import random
from devtinder.users.models import (User, UserLike, RepositorySnippet)
from allauth.socialaccount.models import SocialAccount

AMOUNT_USERS = 10
AMOUNT_REPOS = 10

MIN_LIKES_PER_USER = 1
MAX_LIKES_PER_USER = 10


def init():
    """"""
    username = "test-username-"
    import pdb; pdb.set_trace()
    for i in range(AMOUNT_USERS):
        username += str(User.objects.count())
        user = User.objects.create_user(username=username)
        user.save()
        sa = SocialAccount.objects.create(user=user, uid=str(uuid.uuid4())[:8],
                                          provider='github',
                                          extra_data=get_extra_data())
        sa.save()

    repository = 'test-repo-'
    for i in range(AMOUNT_REPOS):
        repository += str(RepositorySnippet.objects.count())
        owner = User.objects.order_by("?").limit(1)
        language = random.choice(get_languages())
        stars = random.randint(0, 200)
        snippet = get_snippets(language)
        ur = RepositorySnippet.create(owner, repository, language, stars, snippet)
        ur.save()

    for u in User.objects.all():
        for _ in random.randint(MIN_LIKES_PER_USER, MAX_LIKES_PER_USER):
            to_user = User.objects.filter(user__ne=u).order_by("?")
            to_snippet = random.choice(to_user.get_snippets())
            if to_snippet is None:
                break
            # if already gave like, skip
            l = UserLike.objects.filter(from_user=u, to_user=to_user)
            if l.count() == 0:
                like = u.give_like(to_user, to_snippet)
                like.save()

def get_languages():
    return ['python', 'css', 'sass', 'js', 'html']

def get_snippets(language):
    """"""
    snippets = {
        'python': """class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            # possible match
            context['pm'] = user.get_possible_match()
        return context
""",
        'css': """.alert-debug { color: black; background-color: white; border-color: #d6e9c6; }
.alert-error { color: #b94a48; background-color: #f2dede; border-color: #eed3d7; }
@media (max-width: 47.9em) {
  .navbar-nav .nav-item { float: none; width: 100%; display: inline-block; }
  .navbar-nav .nav-item + .nav-item { margin-left: 0; }
  .nav.navbar-nav.pull-xs-right { float: none !important;}
}
[hidden][style="display: block;"] {  display: block !important; }

/* CUSTOM STYLES */
body {
  font-family: 'Raleway', sans-serif;
  color: black;
}
.navbar-brand {
  font-weight: lighter;
}
.git {
  font-weight: bold;
  color: #fd5c63;
}""",
        'js': """/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');""",
        'sass': """// Alert colors

$white: #fff;
$mint-green: #d6e9c6;
$black: #000;
$pink: #f2dede;
$dark-pink: #eed3d7;
$red: #b94a48;

////////////////////////////////
		//Alerts//
////////////////////////////////

// bootstrap alert CSS, translated to the django-standard levels of
// debug, info, success, warning, error

.alert-debug {
  background-color: $white;
  border-color: $mint-green;
  color: $black;
}

.alert-error {
  background-color: $pink;
  border-color: $dark-pink;
  color: $red;
""",
        'html': """{% extends "base.html" %}

{% block title %}Page Not found{% endblock %}

{% block content %}
<h1>Page Not found</h1>

<p>This is not the page you were looking for.</p>
{% endblock content %}
""",

    }
    return snippets.get('language', """No Available""")

def get_extra_data():
    return {'public_repos': 4, 'site_admin': False, 'subscriptions_url': 'https://api.github.com/users/colobas/subscriptions', 'gravatar_id': '', 'hireable': None, 'id': 12519843, 'followers_url': 'https://api.github.com/users/colobas/followers', 'following_url': 'https://api.github.com/users/colobas/following{/other_user}', 'blog': None, 'followers': 6, 'location': 'Portugal', 'type': 'User', 'email': 'gpires@tutanota.com', 'bio': "MSc Electrical and Computer Engineering student at T\\u00e9cnico Lisboa, Portugal.\r\nI'm into solving problems in code.", 'gists_url': 'https://api.github.com/users/colobas/gists{/gist_id}', 'company': None, 'events_url': 'https://api.github.com/users/colobas/events{/privacy}', 'html_url': 'https://github.com/colobas', 'updated_at': '2016-10-04T07:55:56Z', 'received_events_url': 'https://api.github.com/users/colobas/received_events', 'starred_url': 'https://api.github.com/users/colobas/starred{/owner}{/repo}', 'public_gists': 1, 'name': 'Guilherme Pires', 'organizations_url': 'https://api.github.com/users/colobas/orgs', 'url': 'https://api.github.com/users/colobas', 'created_at': '2015-05-19T22:09:43Z', 'avatar_url': 'https://avatars.githubusercontent.com/u/12519843?v=3', 'repos_url': 'https://api.github.com/users/colobas/repos', 'following': 5, 'login': 'colobas'}