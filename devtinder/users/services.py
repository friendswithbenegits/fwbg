# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 10/7/16"""
__author__ = "andresilva"
__email__ = "andre@unbabel.com"

import requests
import base64
import json

def get_data(url, user):
    """Currently we need to return the following json"""
    langs = {
        '.c': 'C',
        '.cpp': 'C++',
        '.cs': 'C#',
        '.css': 'CSS',
        '.go': 'Go',
        '.html': 'HTML',
        '.java': 'Java',
        '.js': 'JavaScript',
        '.php': 'PHP',
        '.py': 'Python',
        '.rb': 'Ruby'
    }
    message = "Okay"
    api_url, repo, handler, contents = convert_github_html_url_to_api_url(url)

    if handler != user.username:
        raise Exception("You can't add a snippet of other people's code! 😓")

    response = requests.get(api_url, auth=("friendwithnobenegits", "pixeldevtinder1"))
    if response.status_code != 200:
        raise Exception("Repository is not public.")
    file = base64.b64decode(response.json().get('content'))

    maxlines = 20
    startline = 0
    endline = startline+maxlines

    try:
        print url
        if '#' in url:
            lines = url[url.find("#")+1:]
            if '-' in lines:
                endline = int(lines[lines.find('-')+2:])
                startline = int(lines[1:lines.find('-')]) - 1
                if startline >= endline:
                    startline = endline - 20
            else:
                startline = int(lines[1:]) - 1
                endline = startline+maxlines
    except Exception, e:
        print e

    # limit lines of code
    file = "\n".join(file.split('\n')[startline:endline])
    if file == "":
        startline = 0
        endline = startline+maxlines
        file = "\n".join(file.split('\n')[0:endline])
    lines = 'L{}-L{}'.format(startline, endline)
    print lines
    print file

    language = contents.split("#")[0].split(".")[-1]
    language = langs.get('.{}'.format(language), None)
    if not language:
        print "Language \"{}\" does not exists. Query for repo language".format(contents.split("#")[0].split(".")[-1])
        r = requests.get('https://api.github.com/repos/{0}/{1}'.format(user.username, repo), auth=("friendwithnobenegits", "pixeldevtinder1"))
        repository = r.json()
        language  = repository.get('language')

    return {
        'message': message,
        'name': repo,
        'filename' : response.json().get('name'),
        'stars': response.json().get('size'),
        'lines': lines,
        'language': language,
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
    return github_url, repo, handler, contents
