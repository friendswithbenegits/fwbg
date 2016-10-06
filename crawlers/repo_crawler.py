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
			files.append(ls.path)
                        print "{0}".format(top_path)

def crawl_repo(repo):
        files = []
        crawl_files("/", files, repo)
        return files