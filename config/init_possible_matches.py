# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 10/6/16"""
__author__ = "andresilva"
__email__ = "andre@unbabel.com"


def init():
    """"""
    pm = {
        'to_user': {
            'handler': '@andreffs18',
            'username': 'andreffs18'
        },
        'repo': {
            'name': 'Sucky project',
            'snippet': """
            def store_person(person):
                try:
                    p_repos = []
                    for repo in person.get_repos():
                    if repo.owner.name == person.name:
                        p_repos.append({
                            "repo_name" : repo.name,
                            "repo_url" : repo.html_url,
                            "repo_id" : repo.id"""
        },
    }
