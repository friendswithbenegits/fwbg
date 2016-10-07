# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 10/7/16"""
__author__ = "andresilva"
__email__ = "andre@unbabel.com"

import requests
import base64

def get_data(url):
    """Currently we need to return the following json"""
    message = "Okay"
    api_url = convert_github_html_url_to_api_url(url)
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("Repository is not public.")
    file = base64.b64decode(response.json().get('content'))

    return {
        'message': message,
        'name': response.json().get('name'),
        'stars': response.json().get('size'),
        'language': 0,
        'snippet': file
    }

def convert_github_html_url_to_api_url(url):
    # url = "https://github.com/andreffs18/collective-intelligence/blob/master/Chapter%202%20-%20Making%20Recomendations/recommendations.py#L5"
    # extract keywords from given html url
    black_list = ['blob', 'https', '', None]
    url_parts = filter(lambda x: x not in black_list, url.split("/"))
    handler = url_parts[2]
    repo = url_parts[3]
    branch = url_parts[4]
    contents = "/".join(url_parts[5:])
    line = contents.split("#")[-1]
    # create valid github api url
    github_url = ("https://api.github.com/repos/{}/{}/contents/{}?ref={}").format(handler, repo, contents, branch)
    return github_url
