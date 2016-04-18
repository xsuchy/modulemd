# -*- coding: utf-8 -*-


# Copyright (c) 2016  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Petr Šabata <contyk@redhat.com>

"""Module metadata manipulation library.

A python3 library for manipulation of the proposed module metadata format.

Example usage:

.. code:: python

    import modulemd
    mmd = modulemd.ModuleMetadata()
    mmd.load("metadata.yaml")
    mmd.add_module_license("ISC")
    mmd.components.rpms.clear_packages()
    mmd.components.rpms.add_package("example", multilib=["x86_64"])
    mmd.dump("out.yaml")
"""

import yaml

from modulemd.components import ModuleComponents
from modulemd.content import ModuleContent
from modulemd.rpms import ModuleRPMs

supported_mdversions = ( 0, )

class ModuleMetadata(object):
    """Class representing the whole module."""

    def __init__(self):
        """Creates a new ModuleMetadata instance."""
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
        """Loads a metadata file into the instance.

        :param str f: File name to load
        """
        with open(f, "r") as infile:
            data = infile.read()
        self.loads(data)

    def loads(self, s):
        """Loads metadata from a string.

        :param str s: Raw metadata in YAML
        :raises ValueError: If the metadata is invalid or unsupported.
        """
        yml = yaml.safe_load(s)
        if yml["document"] != "modulemd":
            raise ValueError("The supplied data isn't a valid modulemd document")
        if yml["version"] not in supported_mdversions:
            raise ValueError("The supplied metadata version isn't supported")
        self.mdversion = yml["version"]
        self.name = yml["data"]["name"]
        self.version = yml["data"]["version"]
        self.summary = yml["data"]["summary"]
        self.description = str(yml["data"]["description"]).strip()
        self.module_licenses = set(yml["data"]["license"]["module"])
        if "content" in yml["data"]["license"]:
            self.content_licenses = set(yml["data"]["license"]["content"])
        if "requires" in yml["data"]:
            self.requires = yml["data"]["requires"]
        if "references" in yml["data"]:
            if "community" in yml["data"]["references"]:
                self.community = yml["data"]["references"]["community"]
            if "documentation" in yml["data"]["references"]:
                self.documentation = yml["data"]["references"]["documentation"]
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
        """Dumps the metadata into the supplied file.

        :param str f: File name of the destination
        """
        data = self.dumps()
        with open(f, "w") as outfile:
            outfile.write(data)

    def dumps(self):
        """Dumps te metadata into a string.

        :rtype: str
        :raises Exception: If metadata validation fails
        """
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
        if self.components:
            data["data"]["components"] = dict()
            if self.components.rpms:
                data["data"]["components"]["rpms"] = dict()
                data["data"]["components"]["rpms"]["dependencies"] = \
                    self.components.rpms.dependencies
                data["data"]["components"]["rpms"]["fulltree"] = \
                    self.components.rpms.fulltree
                if self.components.rpms.packages:
                    data["data"]["components"]["rpms"]["packages"] = dict()
                    for p, e in self.components.rpms.packages.items():
                        extra = dict()
                        if isinstance(e, dict):
                            if "arches" in e:
                                extra["arches"] = e["arches"]
                            if "multilib" in e:
                                extra["multilib"] = e["multilib"]
                        data["data"]["components"]["rpms"]["packages"][p] = \
                            extra
        return yaml.dump(data)

    def validate(self):
        """Performs an in-depth validation of the metadata instance.

        :rtype: bool
        """
        # TODO: do some actual validation
        return True

    @property
    def mdversion(self):
        """An int property representing the metadata format version used.

        This is automatically set to the highest supported version for
        new objects or set by the loaded document.  This value can be
        changed to one of the supported_mdversions to alter the output
        format.
        """
        return self._mdversion

    @mdversion.setter
    def mdversion(self, i):
        if i not in supported_mdversions:
            raise ValueError("Unsupported metadata version")
        self._mdversion = int(i)

    @property
    def name(self):
        """A string property representing the name of the module."""
        return self._name

    @name.setter
    def name(self, s):
        self._name = str(s)

    @property
    def version(self):
        """A string property representing the version of the module."""
        return self._version

    @version.setter
    def version(self, s):
        self._version = str(s)

    @property
    def summary(self):
        """A string property representing a short summary of the module."""
        return self._summary

    @summary.setter
    def summary(self, s):
        self._summary = str(s)

    @property
    def description(self):
        """A string property representing a detailed description of the
        module."""
        return self._description

    @description.setter
    def description(self, s):
        self._description = str(s)

    @property
    def module_licenses(self):
        """A set of strings, a property, representing the license terms
        of the module itself."""
        return self._module_licenses

    @module_licenses.setter
    def module_licenses(self, ss):
        if not isinstance(ss, set):
            raise TypeError("module_licenses requires a set")
        self._module_licenses = ss

    def add_module_license(self, s):
        """Adds a module license to the set.

        :param str s: License name
        """
        self._module_licenses.add(str(s))

    def del_module_license(self, s):
        """Removes the supplied license from the module licenses set.

        :param str s: License name
        """
        self._module_licenses.discard(str(s))

    def clear_module_licenses(self):
        """Clears the module licenses set."""
        self._module_licenses.clear()

    @property
    def content_licenses(self):
        """A set of strings, a property, representing the license terms
        of the module contents."""
        return self._content_licenses

    @content_licenses.setter
    def content_licenses(self, ss):
        if not isinstance(ss, set):
            raise TypeError("content_licenses requires a set")
        self._content_licenses = ss

    def add_content_license(self, s):
        """Adds a content license to the set.

        :param str s: License name
        """
        self._content_licenses.add(str(s))

    def del_content_license(self, s):
        """Removes the supplied license from the content licenses set.

        :param str s: License name
        """
        self._content_licenses.discard(str(s))

    def clear_content_licenses(self):
        """Clears the content licenses set."""
        self._content_licenses.clear()

    @property
    def requires(self):
        """A dictionary property representing the required dependencies of
        the module.

        Keys are the required module names (strings), values are their
        mininum required versions (also strings).
        """
        return self._requires

    @requires.setter
    def requires(self, d):
        if d and not isinstance(d, dict):
            raise TypeError("Incorrect data type passed for requires")
        self._requires = d

    def add_requires(self, n, v):
        """Adds a required module dependency.

        :param str n: Required module name
        :param str v: Required module version
        """
        self._requires[str(n)] = str(v)

    update_requires = add_requires

    def del_requires(self, n):
        """Deletes the dependency on the supplied module.

        :param str n: Required module name
        """
        if str(n) in self._requires:
            del self._requires[str(n)]

    def clear_requires(self):
        """Removes all the dependencies."""
        self._requires = dict()

    @property
    def community(self):
        """A string property representing a link to the upstream community
        for this module."""
        return self._community

    @community.setter
    def community(self, s):
        self._community = str(s)

    @property
    def documentation(self):
        """A string property representing a link to the upstream
        documentation for this module."""
        return self._documentation

    @documentation.setter
    def documentation(self, s):
        self._documentation = str(s)

    @property
    def tracker(self):
        """A string property representing a link to the upstream bug tracker
        for this module."""
        return self._tracker

    @tracker.setter
    def tracker(self, s):
        self._tracker = str(s)

    @property
    def components(self):
        """A ModuleComponents instance property representing the components
        defining the module."""
        return self._components

    @components.setter
    def components(self, o):
        if o and not isinstance(o, ModuleComponents):
            raise TypeError("Incorrect data type passed for components")
        self._components = o
