# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django import forms

from .models import User, UserMatch, Message

class RepoUrlInputFrom(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        url = self.cleaned_data['url']
        if 'github' not in url:
            raise forms.ValidationError("Ooohh, that is not a valid url")
        return url


class MessageInputForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    from_user = forms.CharField(widget=forms.HiddenInput())
    match = forms.CharField(widget=forms.HiddenInput())

    def clean_content(self):
        content = self.cleaned_data['content']
        if content.strip() in ['', None, False, True]:
            raise forms.ValidationError("Ooohh, that is not a valid message.")
        return content

    def clean_from_user(self):
        username_id = self.cleaned_data['from_user']
        try:
            User.objects.get(id=username_id)
        except Exception, e:
            raise forms.ValidationError("User {} does not exist.".format(
                username_id))
        return username_id

    def execute(self, from_user, to_user, content, match_id):
        """"""
        from_user = User.objects.get(id=from_user)
        match = UserMatch.objects.get(id=match_id)
        msg = Message.create(from_user, to_user, content, match)
        msg.save()
        return msg
