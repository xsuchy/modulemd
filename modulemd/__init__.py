import yaml

"""
...
"""

supported_mdversions = ( 0, )

class ModuleMetadata():
	def load(self, f):
		"""
		...
		"""

	def loads(self, s):
		"""
		...
		"""
		yml = yaml.safe_load(s)
		self.mdversion = yml["version"]
		self.version = yml["data"]["version"]

	def dump(self, f):
		"""
		...
		"""

	def dumps(self):
		"""
		...
		"""

	@property
	def mdversion(self):
		return self._mdversion

	@mdversion.setter
	def mdversion(self, i):
		if i not in supported_mdversions:
			raise ValueError("Unsupported metadata version:", i)
		self._mdversion = i

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, s):
		if not s:
			raise ValueError("Missing a required field: name")
		self._name = s

	@property
	def version(self):
		return self._version

	@version.setter
	def version(self, s):
		if not s:
			raise ValueError("Missing a required field: version")
		self._version = s

	@property
	def summary(self):
		return self._summary

	@summary.setter
	def summary(self, s):
		if not s:
			raise ValueError("Missing a required field: summary")
		self._summary = s

	@property
	def description(self):
		return self._description

	@description.setter
	def description(self, s):
		if not s:
			raise ValueError("Missing a required field: description")
		self._description = s

	@property
	def module_licenses(self):
		return self._module_licenses

	@module_licenses.setter
	def module_licenses(self, sl: list):
		# TODO: Check whether it's actually a list of strings
		if not isinstance(sl, list):
			raise ValueError("module_licenses needs to be a list")
		self._module_licenses = sl

	@property
	def content_licenses(self):
		return self._content_licenses

	@content_licenses.setter
	def content_licenses(self, sl):
		if not sl:
			raise ValueError("Missing a required field: content licenses")
		# TODO: Check whether ti's actually a list of strings
		if not isinstance(sl, list):
			raise ValueError("content_licenses needs to be a list")
		self._content_licenses = sl

	@property
	def requires(self):
		return self._requires

	@requires.setter
	def requires(self, d):
		if not isinstance(d, dict):
			raise ValueError("requires needs to be a dictionary")
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
