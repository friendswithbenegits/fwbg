from github import *
import json
import traceback

def store_person(person, f_people): #nome, avatar, email, empresa, location, repos, n_followers, url
	p_repos = []
	for repo in person.get_repos():
		if repo.owner.name == person.name:
			p_repos.append({
				"repo_name" : repo.name,
				"repo_url" : repo.html_url
			})

	p_dict = {
		"name" : person.name,
		"avatar_url" : person.avatar_url,
		"url" : person.html_url,
		"email" : person.email,
		"company" : person.company,
		"location" : person.location,
		"repos" : p_repos,
		"num_followers" : person.followers
	}

	f_people.write(json.dumps(p_dict)+"\n")
	
	print u"Stored person: {0}".format(p_dict["name"])
	
	return

def store_repo(repo, f_repos): #nome, n_contribuidores, linguagens, stars, url
	langs = repo.get_languages()

	r_dict = {
		"name" : repo.name,
		"url" : repo.html_url,
		"languages" : langs,
		"stats" : repo.stargazers_count
	}

	f_repos.write(json.dumps(r_dict)+"\n")

	print u"Stored repo: {0}".format(r_dict["name"])

	return

with open("login.key", "r") as f:
	lines = f.read().splitlines()

g = Github(lines[0], lines[1])
pixels = g.get_organization("PixelsCamp")
pixel_repos = pixels.get_repos()

for repo in pixel_repos:
	try:
		for person in repo.get_contributors():
			f_people = open('people.json','a')
			try:
				store_person(person, f_people)
				for rep in person.get_repos():
					if repo.owner.name == person.name:
						f_repos = open('repos.json', 'a')
						try:
							store_repo(rep, f_repos)
						except:
							print "failed to store repo of {0}".format(person.name)
							traceback.print_exc()
						finally:
							f_repos.close()

			except:
				print "failed to store person and its repos"
				traceback.print_exc()
			finally:
				f_people.close()
	except:
		print "failed to store pixels camp repo {0} and its contributors".format(repo)
		traceback.print_exc()