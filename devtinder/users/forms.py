# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django import forms

class RepoUrlInputFrom(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        url = self.cleaned_data['url']
        if 'github' not in url:
            raise forms.ValidationError("Ooohh, that is not a valid url")
        return url