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

class Parser():
	def __init__(self, language):
		self.language = language

	def extract_snippet(self, file_content):
		return "blablabla"