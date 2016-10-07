from github_interface import *
from code_parser import Parser

langs = {
		"JavaScript" : ".js",
		"Java" : ".java",
		"Python" : ".py",
		"Ruby" : ".rb",
		"PHP" : ".php",
		"C++" : ".cpp",
		"CSS" : ".css",
		"C#" : ".cs",
		"C" : ".c",
		"Go" : ".go",
		"HTML" : ".html"
}

def get_snippet(file, lang):
	p = Parser(lang)
	return p.extract_snippet(file)


def get_repo_snippet(repo, username, password):
	global langs
	files = []

	if repo["language"] in langs:
		ext = langs[repo["language"]]
	else:
		ext = ""

	crawl_repo_files("", files, repo, ext, username, password)
	
	f = []
	for file in files:
		if "content" in file:
			f.append(file)

	file = max(f, key=lambda x: len(x["content"]))
	snippet, snippet_line = get_snippet(file["content"], repo["language"])

	snippet_url = file["html_url"]+'#L{0}'.format(snippet_line)

	return snippet, snippet_url

def get_user_repos(user_login_name, username, password):
	user_snippets = []

	for repo in get_repos(user_login_name, username, password):
		if repo["owner"]["login"] == user_login_name and repo["language"] != None:
			snippet, snippet_url = get_repo_snippet(repo, username, password)
			repo_dict={
				"repo_name" : repo["name"],
				"repo_url" : repo["html_url"],
				"repo_id" : repo["id"],
				"repo_lang" : repo["language"],
				"repo_snippet_url" : snippet_url,
				"repo_snippet" : snippet
			}
			user_snippets.append(repo_dict)
			print repo_dict

	return user_snippets