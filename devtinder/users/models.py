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

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_github_account(self):
        """Wrapper that gets content first oauth authentication"""
        sa = SocialAccount.objects.get(user=self)
        return sa.extra_data

    # region Actions
    def give_like(self, to_user, repo):
        """Method to give like to given user from "self" user.
        This will create a new UserLike"""
        like = UserLike.objects.create(
            from_user=self, to_user=to_user, repo=repo)
        return like
    
    def give_dislike(self, to_user, repo):
        """Method to give like to given user from "self" user.
        This will create a new UserLike"""
        dislike = UserDislike.objects.create(
            from_user=self, to_user=to_user, repo=repo)
        return dislike

    # endregion


class UserMatch(models.Model):
    """"""
    user1 = models.ForeignKey(User)
    user2 = models.ForeignKey(User)


class UserLike(models.Model):
    """"""
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)
    create_date = models.DateTimeField(_('creation date'),
                                       default=timezone.now)

    @classmethod
    def get_likes_from(cls, user):
        """Get all likes from give user"""
        return cls.objects.filter(from_user=user)


class UserDislike(models.Model):
    """"""
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)
    create_date = models.DateTimeField(_('creation date'),
                                       default=timezone.now)

    @classmethod
    def get_dislikes_from(cls, user):
        """Get all dislikes from give user"""
        return cls.objects.filter(from_user=user)


class UserRepository(models.Model):
    """"""
    owner = models.ForeignKey(User)
    language = models.CharField()
