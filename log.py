import collections
import os.path

class run:
	def __init__(self, tool, inputs = [], outputs = [], args = []):
		self.tool = tool
		self.inputs = inputs
		self.outputs = outputs
		self.args = args

		if run.src_root:
			self.inputs = [ s.replace(run.src_root, '') for s in inputs ]

	def add_input(self, input_file):
		if run.src_root: input_file = input_file.replace(run.src_root, '')
		self.inputs.append(os.path.normpath(input_file))

	def add_output(self, output_file): self.outputs.append(output_file)

	src_root = None
	@classmethod
	def set_src_root(cls, root):
		cls.src_root = root

	def __str__(self):
		return '%s %s > %s' % (
			self.tool,
			' '.join([ os.path.basename(i) for i in self.inputs ]),
			', '.join(self.outputs))


class crun(run):
	def __init__(self, args, tool = 'cc'):
		super().__init__(tool, [], [], [])

		self.defines = []
		self.includes = []
		self.libraries = []
		self.libdirs = []
		self.flags = []

		args = collections.deque(args)
		while len(args) > 0:
			arg = args.popleft()

			for (prefix,handler) in (
					('-I', self.add_include),
					('-L', self.add_libdir),
					('-l', self.add_lib)):
				if arg.startswith(prefix):
					l = len(prefix)
					if len(arg) > l: handler(arg[l:])
					else: handler(args.popleft())

					arg = None
					break

			if arg is None: continue
			elif arg == '-o': self.add_output(args.popleft())
			elif arg.startswith('-'): self.add_flag(arg)
			else: self.add_input(arg)

		for infile in self.inputs:
			(base, ext) = os.path.splitext(os.path.basename(infile))
			if len(self.outputs) == 0:
				self.add_output('%s.o' % base)

	def add_include(self, incdir): self.includes.append(incdir)
	def add_libdir(self, libdir): self.libdirs.append(libdir)
	def add_lib(self, lib): self.libraries.append(lib)
	def add_flag(self, f): self.flags.append(f)

	def __repr__(self):
		return '%s %s %s -I %s -l %s -L %s -o %s' % (
			self.tool, self.inputs, self.flags, self.includes,
			self.libraries, self.libdirs, self.outputs
		)


class cxxrun(crun):
	def __init__(self, args):
		super().__init__(args, tool = 'c++')


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
