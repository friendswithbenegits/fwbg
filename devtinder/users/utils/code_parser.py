from random import *
from base64 import b64decode

def general(file):
	file = file.splitlines()
	if len(file) > 5:
		i = randint(0,len(file)-5)
		rng = min([len(file)-i, 4])
		file = file[i:i+rng]
		return trim_whitespace(file), i+1
	else:
		return trim_whitespace(file), 1

def trim_whitespace(file):
	while file[0] == "" or file[len(file)-1] == "":
		if file[0] == "":
			file = file[1:]

		if file[len(file)-1] == "":
			file = file[:-1]


	return '\n'.join(file)+'\n'


langs = {
		"JavaScript" : ["function", "if", "while", "for"],
		"Java" : ["class", "if", "while", "for", "interface"],
		"Python" : ["class", "def", "if", "while", "for"],
		"Ruby" : ["if", "for", "each", "while", "begin", "def", "class"],
		"PHP" : ["if", "for", "switch", "while", "do", "function", "class"],
		"C++" : ["){", "if", "while", "switch", "for", "{", "namespace", "class"],
		"CSS" : ["{", "@media"],
		"C#" : ["){", "if", "while", "switch", "for", "{", "namespace", "class"],
		"C" : ["){", "if", "while", "for", "{", "switch", "struct", "typedef", "select"],
		"Go" : ["func", "if", "while", ",switch", "for", ":\n", "interface", "struct"],
		"HTML" : ["<div>", "<script", "<body", "<"]
}




class Parser():
	def __init__(self, language):
		global langs
		if language in langs:
			self.lang_keywords = langs[language]
		else:
			self.lang_keywords = []

	def extract_snippet(self, file_content):
		file_content = b64decode(file_content)
		lines = file_content.splitlines()

		if len(self.lang_keywords) > 0:
			first_lines = [lines.index(line) for line in lines if any(word in line for word in self.lang_keywords)]

			if len(first_lines) > 0:
				i = random.choice(first_lines)
				rng = min([len(file)-i, 4])
				file = file[i:i+rng]
				return trim_whitespace(file), i+1
			else:
				return general(file_content)
		else:
			return general(file_content)