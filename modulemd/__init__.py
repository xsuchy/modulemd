import yaml

supported_mdversions = ( 0, )

class ModuleMetadata():
	def __init__(self):
		self.mdversion = max(supported_mdversions)
		self.name = None
		self.version = None
		self.summary = None
		self.description = None
		self.module_licenses = []
		self.content_licenses = []
		self.requires = dict()
		self.community = None
		self.documentation = None
		self.tracker = None

	def load(self, f):
		with open(f, "r") as infile:
			data = infile.read()
		self.loads(data)

	def loads(self, s):
		yml = yaml.safe_load(s)
		if yml["document"] != "modulemd":
			raise ValueError("The supplied data isn't a valid modulemd document")
		if yml["version"] not in supported_mdversions:
			raise ValueError("The supplied metadata version isn't supported")
		self.mdversion = yml["version"]
		self.name = yml["data"]["name"]
		self.version = yml["data"]["version"]
		self.summary = yml["data"]["summary"]
		self.description = yml["data"]["description"]
		self.module_licenses = yml["data"]["license"]["module"]
		if "content" in yml["data"]["license"]:
			self.content_licenses = yml["data"]["license"]["content"]
		if "requires" in yml["data"]:
			self.requires = yml["data"]["requires"]
		if "references" in yml["data"]:
			if "community" in yml["data"]["references"]:
				self.community = yml["data"]["references"]["community"]
			if "documentation" in yml["data"]["references"]:
				self.document = yml["data"]["references"]["documentation"]
			if "tracker" in yml["data"]["references"]:
				self.tracker = yml["data"]["references"]["tracker"]
		# TODO: components

	def dump(self, f):
		data = self.dumps()
		with open(f, "w") as outfile:
			outfile.write(data)

	def dumps(self):
		if not self.validate:
			raise Exception("Metadata validation failed")
		data = dict()
		# header
		data["document"] = "modulemd"
		data["version"] = self.mdversion
		# data
		data["data"] = dict()
		data["data"]["name"] = self.name
		data["data"]["version"] = self.version
		data["data"]["summary"] = self.summary
		data["data"]["description"] = self.description
		data["data"]["license"] = dict()
		data["data"]["license"]["module"] = self.module_licenses
		if self.content_licenses:
			data["data"]["license"]["content"] = self.content_licenses
		if self.requires:
			data["data"]["requires"] = self.requires
		if self.community or self.documentation or self.tracker:
			data["data"]["references"] = dict()
			if self.community:
				data["data"]["references"]["community"] = self.community
			if self.documentation:
				data["data"]["references"]["documentation"] = self.documentation
			if self.tracker:
				data["data"]["references"]["tracker"] = self.tracker
		# TODO: components
		return yaml.dump(data)

	def validate(self):
		# TODO: do some actual validation
		return True


	@property
	def mdversion(self):
		return self._mdversion

	@mdversion.setter
	def mdversion(self, i):
		self._mdversion = i

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, s):
		self._name = s

	@property
	def version(self):
		return self._version

	@version.setter
	def version(self, s):
		self._version = s

	@property
	def summary(self):
		return self._summary

	@summary.setter
	def summary(self, s):
		self._summary = s

	@property
	def description(self):
		return self._description

	@description.setter
	def description(self, s):
		self._description = s

	@property
	def module_licenses(self):
		return self._module_licenses

	@module_licenses.setter
	def module_licenses(self, sl: list):
		self._module_licenses = sl

	@property
	def content_licenses(self):
		return self._content_licenses

	@content_licenses.setter
	def content_licenses(self, sl):
		self._content_licenses = sl

	@property
	def requires(self):
		return self._requires

	@requires.setter
	def requires(self, d):
		self._requires = d

	@property
	def community(self):
		return self._community

	@community.setter
	def community(self, s):
		self._community = s

	@property
	def documentation(self):
		return self._documentation

	@documentation.setter
	def documentation(self, s):
		self._documentation = s

	@property
	def tracker(self):
		return self._documentation

	@tracker.setter
	def tracker(self, s):
		self._documentation = s

	# TODO: components not implemented yet
