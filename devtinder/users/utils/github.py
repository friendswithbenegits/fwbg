import requests
import json


exclude_keywords = ["log", "test", "setup", "config", "dot_git", "lib", "image", "images", "graphics", ".png", ".gif", ".pdf", ".jpg", ".ini", ".md"]

def exclude_paths(path):
	global exclude_keywords

	for keyword in exclude_keywords:
		if keyword in path:
			return True

	return False

def get_repos(user, username, password):
	r = requests.get('https://api.github.com/users/{0}/repos'.format(user), auth=(username, password))
	return json.loads(r._content)

def get_contents(path, repo, username, password): #when called on a file returns a json that includes the encoded content
	r = requests.get("https://api.github.com/repos/{0}/{1}/contents/{2}".format(repo["owner"]["login"], repo["name"], path), auth=(username, password))
	return json.loads(r._content)

def crawl_repo_files(path, files, repo, ext, username, password):
	print path
	ls = get_contents(path, repo, username, password)

	for item in ls:
		if not exclude_paths(item["path"]):
			if item["type"] == "dir":
				crawl_repo_files(item["path"], files, repo, ext, username, password)
			else:
				if ext == "" :
					files.append(get_contents(item["path"],repo, username, password))
				elif item["name"][-len(ext):] == ext:			 
					files.append(get_contents(item["path"],repo, username, password))