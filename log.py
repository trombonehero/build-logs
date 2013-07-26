class diag:
	def __init__(self, filename, line, column, message):
		self.filename = filename
		self.line = line
		self.column = column
		self.message = message
		self.notes = []
		self.codelines = []
		self.suggestions = []

	def add_note(self, filename, line, column, message):
		self.notes.append(diag(filename, line, column, message))

	def add_code(self, line, caret_line = None):
		self.codelines.append((line, caret_line))

	def add_suggestion(self, line):
		self.suggestions.append(line)

class run:
	def __init__(self, *args, inputs = [], outputs = []):
		self.args = args
		self.inputs = inputs
		self.outputs = outputs
