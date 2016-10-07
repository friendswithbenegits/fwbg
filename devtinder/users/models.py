# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


from allauth.socialaccount.models import SocialAccount

@python_2_unicode_compatible
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    # Is set to true when a new editor signins with github.
    has_signup = models.BooleanField(default=False)

    @property
    def languages(self):
        """property that returns list of languages from all repos that this
        user has"""
        return UserRepository.objects.filter(owner=self).distinct('language')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_github_account(self):
        """Wrapper that gets content first oauth authentication"""
        sa = SocialAccount.objects.get(user=self)
        return sa.extra_data

    # region Actions
    def give_like(self, to_user):
        """Method to give like to given user from "self" user.
        This will create a new UserLike"""
        like = UserLike.create(from_user=self, to_user=to_user)
        like.save()

        # check if there is any likes from the other way around
        like_back = UserLike.objects.filter(from_user=to_user, to_user=self)
        if like_back.count() != 0:
            # somene already like me, create UserMatch
            um = UserMatch.get_or_create(user1=self, user2=to_user)
            um.save()

        return like

    def give_dislike(self, to_user):
        """Method to give like to given user from "self" user.
        This will create a new UserLike"""
        dislike = UserDislike.create(from_user=self, to_user=to_user)
        dislike.save()
        return dislike
    # endregion

    # region Frontend Action Triggers
    def get_possible_match(self):
        """Return possible match for this user"""
        users = User.objects.exclude(id=self.id)
        repositories = UserRepository.objects.filter(
            owner__in=users, language__in=self.languages)

        UserLike.objects.filter()
        UserDislike.objects.filter()
        UserMatch.objects.filter()

        repositories.exclude()
        return {
            'to_user': {
                'handler': '@andreffs18',
                'username': 'andreffs18',
                'avatar': 'https://avatars2.githubusercontent.com/u/5011530?v=3&s=400'
            },
            'repo': {
                'name': 'Sucky project',
                'stars': 50,
                'snippet': {
                    'text': """def store_person(person):
    try:
        p_repos = []
        for repo in person.get_repos():
        if repo.owner.name == person.name:
            p_repos.append({
                "repo_name" : repo.name,
                "repo_url" : repo.html_url,
                "repo_id" : repo.id""",
                    'lang': 'python',
                    'file': 'main.py',
                    'lines': '10-15'
                }
            },
        }


    # endregion



class UserMatch(models.Model):
    """"""
    user1 = models.ForeignKey(User, related_name="user_match_user1")
    user2 = models.ForeignKey(User, related_name="user_match_user2")

    @classmethod
    def get_or_create(cls, user1, user2):
        """"""
        um = cls.objects.filter(user1=user1, user2=user2).first()
        if um is not None:
            um = cls.objects.create(user1=user1, user2=user2)
            um.save()
        return um


class UserLike(models.Model):
    """"""
    from_user = models.ForeignKey(User, related_name="user_like_from_user")
    to_user = models.ForeignKey(User, related_name="user_like_to_user")
    create_date = models.DateTimeField(_('creation date'),
                                       default=timezone.now)

    @classmethod
    def create(cls, from_user, to_user):
        """"""
        ul = cls.objects.create(from_user=from_user, to_user=to_user)
        ul.save()
        return ul

    @classmethod
    def get_likes_from(cls, user):
        """Get all likes from give user"""
        return cls.objects.filter(from_user=user)


class UserDislike(models.Model):
    """"""
    from_user = models.ForeignKey(User, related_name="user_dislike_from_user")
    to_user = models.ForeignKey(User, related_name="user_dislike_to_user")
    create_date = models.DateTimeField(_('creation date'),
                                       default=timezone.now)

    @classmethod
    def create(cls, from_user, to_user):
        """"""
        ud = cls.objects.create(from_user=from_user, to_user=to_user)
        ud.save()
        return ud

    @classmethod
    def get_dislikes_from(cls, user):
        """Get all dislikes from give user"""
        return cls.objects.filter(from_user=user)


class UserRepository(models.Model):
    """"""
    owner = models.ForeignKey(User)
    language = models.CharField(max_length=124)
    starts = models.IntegerField(default=0)

    @classmethod
    def create(cls, owner, language):
        """"""
        ur = cls.objects.create(owner=owner, language=language)
        ur.save()
        return ur


class RepositorySnippet(models.Model):
    """"""
    snippet = models.TextField()

    @classmethod
    def create(cls, snippet):
        """"""
        rs = cls.objects.create(snippet=snippet)
        rs.save()
        return rs