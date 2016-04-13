import yaml

supported_mdversions = ( 0, )

class ModuleMetadata():
	def __init__(self):
		self.mdversion = max(supported_mdversions)
		self.name = None
		self.version = None
		self.summary = None
		self.description = None
		self.module_licenses = set()
		self.content_licenses = set()
		self.requires = dict()
		self.community = None
		self.documentation = None
		self.tracker = None
		self.components = None

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
		self.description = yml["data"]["description"].strip()
		self.module_licenses = set(yml["data"]["license"]["module"])
		if "content" in yml["data"]["license"]:
			self.content_licenses = set(yml["data"]["license"]["content"])
		if "requires" in yml["data"]:
			self.requires = yml["data"]["requires"]
		if "references" in yml["data"]:
			if "community" in yml["data"]["references"]:
				self.community = yml["data"]["references"]["community"]
			if "documentation" in yml["data"]["references"]:
				self.document = yml["data"]["references"]["documentation"]
			if "tracker" in yml["data"]["references"]:
				self.tracker = yml["data"]["references"]["tracker"]
		if "components" in yml["data"]:
			self.components = ModuleComponents()
			if "rpms" in yml["data"]["components"]:
				self.components.rpms = ModuleRPMs()
				if "dependencies" in yml["data"]["components"]["rpms"]:
					self.components.rpms.dependencies = \
						yml["data"]["components"]["rpms"]["dependencies"]
				if "fulltree" in yml["data"]["components"]["rpms"]:
					self.components.rpms.fulltree = \
						yml["data"]["components"]["rpms"]["fulltree"]
				if "packages" in yml["data"]["components"]["rpms"]:
					for p, e in yml["data"]["components"]["rpms"]["packages"].items():
						extras = dict()
						if e:
							if "arches" in e:
								extras["arches"] = e["arches"]
							if "multilib" in e:
								extras["multilib"] = e["multilib"]
						self.components.rpms.add_package(p, **extras)

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
		data["data"]["license"]["module"] = list(self.module_licenses)
		if self.content_licenses:
			data["data"]["license"]["content"] = list(self.content_licenses)
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
	def module_licenses(self, ss):
		if not isinstance(ss, set):
			raise TypeError("module_licenses requires a set")
		self._module_licenses = ss

	def add_module_license(self, s):
		self._module_licenses.add(s)

	def del_module_license(self, s):
		self._module_licenses.discard(s)

	def clear_module_licenses(self):
		self._module_licenses.clear()

	@property
	def content_licenses(self):
		return self._content_licenses

	@content_licenses.setter
	def content_licenses(self, ss):
		if not isinstance(ss, set):
			raise TypeError("content_licenses requires a set")
		self._content_licenses = ss

	def add_content_license(self, s):
		self._content_licenses.add(s)

	def del_content_license(self, s):
		self._content_licenses.discard(s)

	def clear_content_licenses(self):
		self._content_licenses.clear()

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

	@property
	def components(self):
		return self._components

	@components.setter
	def components(self, o):
		self._components = o

class ModuleComponents():
	def __init__(self):
		self._rpms = None

	@property
	def rpms(self):
		return self._rpms

	@rpms.setter
	def rpms(self, o):
		if not isinstance(o, ModuleRPMs):
			raise TypeError("rpms needs to be an instance of ModuleRPMs")
		self._rpms = o

class ModuleContent():
	def __init__(self):
		self.packages = dict()

	@property
	def packages(self):
		return self._packages

	@packages.setter
	def packages(self, d):
		self._packages = d

	def add_package(self, p):
		pkgs = self._packages
		pkgs[p] = None
		self.packages = pkgs

	update_package = add_package

	def del_package(self, p):
		if p in self._packages:
			del self._packages[p]

	def clear_packages(self):
		self._packages = dict()


class ModuleRPMs(ModuleContent):
	def __init__(self):
		self._dependencies = True
		self._fulltree = True
		self._packages = dict()

	def add_package(self, p, arches=None, multilib=None):
		pkgs = self._packages
		pkgs[p] = None
		if arches or multilib:
			pkgs[p] = dict()
			if arches:
				pkgs[p]["arches"] = arches
			if multilib:
				pkgs[p]["multilib"] = multilib
		self.packages = pkgs

	@property
	def dependencies(self):
		return self._dependencies

	@dependencies.setter
	def dependencies(self, b):
		self._dependencies = b

	@property
	def fulltree(self):
		return self._fulltree

	@fulltree.setter
	def fulltree(self, b):
		self._fulltree = b
