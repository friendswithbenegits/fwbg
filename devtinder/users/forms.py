# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django import forms
from .models import User, Message, UserMatch

class RepoUrlInputFrom(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        url = self.cleaned_data['url']
        if 'github' not in url:
            raise forms.ValidationError("Ooohh, that is not a valid url")
        return url



class MessageInputForm(forms.Form):
    content = forms.TextInput()
    to_user = forms.CharField(widget=forms.HiddenInput())
    match = forms.CharField(widget=forms.HiddenInput())

    def clean_content(self):
        content = self.cleaned_data['content']
        if content.strip() in ['', None, False, True]:
            raise forms.ValidationError("Ooohh, that is not a valid message.")
        return content

    def clean_to_user(self):
        username = self.cleaned_data['to_user']
        try:
            User.objects.get(username=username)
        except Exception, e:
            raise forms.ValidationError("User {} does not exist.".format(
                username))
        return username

    def execute(self, from_user, to_user, content, match_id):
        """"""
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        match = UserMatch.objects.get(id=match_id)
        msg = Message.create(to_user, from_user, content, match)
        msg.save()
        return msg
