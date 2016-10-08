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
    def handler(self):
        """return twitter handler"""
        return "@{}".format(self.name)

    @property
    def location(self):
        """"""
        return self.get_github_account().get('location')

    @property
    def avatar_url(self):
        """"""
        return self.get_github_account().get('avatar_url')

    @property
    def languages(self):
        """property that returns list of languages from all repos that this
        user has"""
        return list(RepositorySnippet.objects.filter(owner=self).distinct(
            'language').values_list('language', flat=True))

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_github_account(self):
        """Wrapper that gets content first oauth authentication"""
        try:
            sa = SocialAccount.objects.get(user=self)
            return sa.extra_data
        except Exception, e:
            print("This shouldn't happen but oh well. User \"{}\" "
                  "doesnt have social account".format(self))
            return {}

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
        print("{} just liked user {}".format(self, to_user))
        return like

    def give_dislike(self, to_user):
        """Method to give like to given user from "self" user.
        This will create a new UserLike"""

        dislike = UserDislike.create(from_user=self, to_user=to_user)
        dislike.save()
        print("{} just disliked user {}".format(self, to_user))
        return dislike

    def get_matches_count(self):
        """"""
        query = (models.Q(user1=self, user1_has_seen=False) |
                 models.Q(user2=self, user2_has_seen=False))
        return UserMatch.objects.filter(query).count()
    # endregion

    def get_all_snippets(self):
        """Get all snippets for each repo from given user"""
        return RepositorySnippet.objects.filter(owner=self)


    # region Frontend Action Triggers
    def get_unseen_matches(self):
        """"""
        matches = UserMatch.objects.filter(user1=self)
        matches = matches.exclude(user1_has_seen=True)
        
        if len(matches) > 0:
            return {
                "status": 200,
                "matches": matches,
                "message": "here you have some matches!"
            }
        else:   
            return {
                "status": 400,
                "matches": [],
                "message": "no matches for you."
            }

    def get_suggestions(self):
        """Return possible match for this user:
        1º - Get all users except myself.
        2º - From all users remove ones that I already gave like or dislike
        3º - and get all their repos that have the same language as I have.
        4º - order repo by stars and get first one"""
        pixelsadmin = User.objects.get(username="pixeladmin").id
        users = User.objects.exclude(id__in=[self.id, pixelsadmin])
        likes = UserLike.objects.filter(
             from_user=self).values_list('to_user', flat=True)
        dislikes = UserDislike.objects.filter(
            from_user=self).values_list('to_user', flat=True)
        users = users.exclude(id__in=list(set(likes).union(set(dislikes))))
        try:
            snippet = RepositorySnippet.objects.filter(
                owner__in=users).order_by("?")[0]
            return {
                'status': 200,
                'message': "Hello",
                'to_user': {
                    'handler': snippet.owner.handler,
                    'username': snippet.owner.username,
                    'location': snippet.owner.location,
                    'avatar_url': snippet.owner.avatar_url,
                },
                'snippet': {
                    'lang': snippet.language,
                    'repository': snippet.repository,
                    'name': snippet.repository,
                    'stars': snippet.stars,
                    'snippet': snippet.snippet,
                    'lines': 10,
                },
            }
        except IndexError, e:
            return {
                'status': 400,
                'message': "Our <span class='git'>git</span> <strong>count-objects</strong> returned 0 for the amount of people you're able to <span class='git'>git</span> <strong>merge</strong> at the moment.",
                'to_user': {},
                'snippet': {},
            }
        # endregion


class UserMatch(models.Model):
    """"""
    user1 = models.ForeignKey(User, related_name="user_match_user1")
    user2 = models.ForeignKey(User, related_name="user_match_user2")
    user1_has_seen = models.BooleanField(default=False)
    user2_has_seen = models.BooleanField(default=False)

    def __unicode__(self):
        """"""
        return "{} & {}".format(self.user1, self.user2)

    @classmethod
    def get_matches(cls, user):
        """"""
        query = (models.Q(user1=user) | models.Q(user2=user))
        return cls.objects.filter(query)

    @classmethod
    def get_or_create(cls, user1, user2):
        """"""
        um = cls.objects.filter(user1=user1, user2=user2).first()
        if um is None:
            um = cls.objects.create(user1=user1, user2=user2)
            um.save()
        return um

    def get_has_seen(self, user):
        """"""
        if self.user1 == user:
            return self.user1_has_seen
        elif self.user2 == user:
            return self.user2_has_seen
        else:
            raise ValueError("User {} does not belong to this UserMatch"
                             "".format(user))

    def mark_as_seen_by(self, user):
        """"""
        if self.user1 == user:
            self.user1_has_seen = True
        elif self.user2 == user:
            self.user2_has_seen = True
        else:
            raise ValueError("User {} does not belong to this UserMatch"
                             "".format(user))
        self.save()


class UserLike(models.Model):
    """"""
    from_user = models.ForeignKey(User, related_name="user_like_from_user")
    to_user = models.ForeignKey(User, related_name="user_like_to_user")
    create_date = models.DateTimeField(_('creation date'),
                                       default=timezone.now)

    meta = {
        'indexes': ['from_user'],
    }

    def __unicode__(self):
        """"""
        return "{} likes {}".format(self.from_user, self.to_user)

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
    meta = {
        'indexes': ['from_user'],
    }

    def __unicode__(self):
        """"""
        return "{} dislikes {}".format(self.from_user, self.to_user)

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


class RepositorySnippet(models.Model):
    """"""
    owner = models.ForeignKey(User)
    repository = models.CharField(max_length=124)
    language = models.CharField(max_length=124)
    filename = models.CharField(max_length=124)
    lines = models.CharField(max_length=124)
    stars = models.IntegerField(default=0)
    snippet = models.TextField()

    meta = {
        'indexes': ['owner'],
    }

    def __unicode__(self):
        return ("{}: Owner {} | Language {} | Stars {}"
                "").format(self.repository, self.owner, self.language,
                           self.stars)

    @classmethod
    def create(cls, owner, repository, language, stars, snippet, lines,
               filename):
        """"""
        rs = cls.objects.create(owner=owner, repository=repository,
                                language=language, stars=stars,
                                filename=filename, snippet=snippet,
                                lines=lines)
        rs.save()
        return rs

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="user_message_from_user")
    to_user = models.ForeignKey(User, related_name="user_message_to_user")
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    match = models.ForeignKey(UserMatch)

    def __unicode__(self):
        return ("From:{} | To:{} | Timestamp:{} | Content:{}"
                "").format(self.from_user.username, self.to_user.username, 
                self.timestamp, self.content)

    @classmethod
    def create(cls, from_user, to_user, content, match):
        msg = cls.objects.create(from_user=from_user, to_user=to_user, content=content, match=match)
        msg.save()

        return msg