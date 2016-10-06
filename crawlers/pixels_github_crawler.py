from github import *
import json
import traceback

def store_person(person): #nome, avatar, email, empresa, location, repos, n_followers, url, id
	try:
		p_repos = []
		for repo in person.get_repos():
			if repo.owner.name == person.name:
				p_repos.append({
					"repo_name" : repo.name,
					"repo_url" : repo.html_url,
					"repo_id" : repo.id
				})
				store_repo(repo)

		p_dict = {
			"name" : person.name,
			"avatar_url" : person.avatar_url,
			"url" : person.html_url,
			"email" : person.email,
			"company" : person.company,
			"location" : person.location,
			"repos" : p_repos,
			"num_followers" : person.followers,
			"id" : person.id
		}

		f_people = open('people.json','a')
		try:
			f_people.write(json.dumps(p_dict)+"\n")
		finally:
			f_people.close()
		
		print u"Stored person: {0}".format(person.name)
	
	except:
		print u"Failed to store person: {0}".format(person.name)

	return

def store_repo(repo): #nome, n_contribuidores, linguagens, stars, url, id
	try:	
		langs = repo.get_languages()

		r_dict = {
			"name" : repo.name,
			"url" : repo.html_url,
			"languages" : langs,
			"stats" : repo.stargazers_count,
			"id" : repo.id
		}

		f_repos = open('repos.json','a')
		try:
			f_repos.write(json.dumps(r_dict)+"\n")
		finally:
			f_repos.close()

		print u"Stored repo: {0}".format(repo.name)
	
	except:
		print u"Failed to store repo: {0}".format(repo.name)
	
	return


with open("login.key", "r") as f:
	lines = f.read().splitlines()

g = Github(lines[0], lines[1])
pixels = g.get_organization("PixelsCamp")
pixel_repos = pixels.get_repos()


for repo in pixel_repos: #all repos in PixelsCamp' GitHub organization...
	for person in repo.get_contributors(): #all contributores in each of those repos...
		store_person(person)
		for rep in person.get_repos(): #each repo owned by each of those contributors...
			for pers in rep.get_contributors(): #each contributor on each of those repos...
				store_person(pers)