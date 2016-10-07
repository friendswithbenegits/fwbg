from github import Github
from code_parser import Parser
import random

langs = {
		"JavaScript" : ".js",
		"Java" : ".java",
		"Python" : ".py",
		"Ruby" : ".rb",
		"PHP" : ".php",
		"C++" : ".cpp",
		"CSS" : ".css",
		"C#" : ".cs",
		"C" : "C",
		"Go" : ".go"
}


def exclude_paths(path):
	keywords = ["log", "test", "setup", "config", "dot_git", "lib"]
	for keyword in keywords:
		if keyword in path:
			return True

	return False

def crawl_files(top_path, files, repo):
	global langs
	ext = langs[repo.language]
	ls = r.get_contents(top_path)

	if exclude_paths(top_path):
		return

	if isinstance(ls, list):
		for path in ls:
			crawl_files(path.path, files, repo)
	else:
		if ls.name[-len(ext):] == ext:			 
			files.append(ls)
#			print "{0}".format(top_path)


def get_snippet(file, lang):
	p = Parser(lang)
	return p.extract_snippet(file)


def get_repo_snippet(repo_id):
	with open("login.key", "r") as f:
			lines = f.read().splitlines()
	g = Github(lines[0], lines[1])
	repo = g.get_repo(repo_id)
	files = []
	crawl_files("/", files, repo)
	file = random.choice(file)
	return get_snippet(file.content, repo.language)


def get_user_repos(user_id):
    with open("login.key", "r") as f:
        lines = f.read().splitlines()
    g = Github(lines[0], lines[1])

    user = g.get_user(user_id)
    user_snippets = []

    for repo in user.get_repos():
        user_snippets.append({
            "repo_name" : repo.name,
            "repo_url" : repo.html_url,
            "repo_id" : repo.id
            "repo_snippet" : get_repo_snippet(repo.id)
        })

    return user_snippets