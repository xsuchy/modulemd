#/usr/bin/python3
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
# Written by Jan Kaluza <jkaluza@redhat.com>

import unittest

import os
import sys

DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(DIR, ".."))

import modulemd
from yaml.scanner import ScannerError

class TestIO(unittest.TestCase):
    def test_invalid_yaml(self):
        document = """
            document: modulemd
            version: 0
            data
        """
        mmd = modulemd.ModuleMetadata()
        self.assertRaisesRegexp(ScannerError,
                                "could not found expected ':'",
                                mmd.loads, document)

    def test_object_value(self, yaml=None, value=""):
        """
        Replaces $VALUE in the the `yaml` input with the value provided
        in the `value` variable and loads the yaml using modulemd library.
        """
        if not yaml:
            return

        yaml = yaml.replace("$VALUE", value)
        mmd = modulemd.ModuleMetadata()
        mmd.loads(yaml)
        mmd.validate()

    def test_object_missing(self, yaml=None):
        """
        Removes the line with the $VALUE from the yaml input and
        loads the yaml using modulemd library.
        """
        if not yaml:
            return

        yaml = "\n".join(n for n in yaml.split("\n") if "$VALUE" not in n)
        mmd = modulemd.ModuleMetadata()
        mmd.loads(yaml)
        mmd.validate()

    def test_document(self):
        document = """
            document: $VALUE
            version: 0
            data:
                name: test
                version: 1.23
                release: 4
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError,
                                "The supplied data isn't a valid modulemd document",
                                self.test_object_missing, document)
        for value in ["", "modulemd2", "[]", "{}"]:
            self.assertRaisesRegexp(ValueError,
                                    "The supplied data isn't a valid modulemd document",
                                    self.test_object_value, document, value)

    def test_version(self):
        document = """
            document: modulemd
            version: $VALUE
            data:
                name: test
                version: 1.23
                release: 4
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError, ".* is required",
                                self.test_object_missing, document)
        for value in ["", "unknown", "[]", "{}", "9999"]:
            self.assertRaisesRegexp(ValueError,
                                    "The supplied metadata version isn't supported",
                                    self.test_object_value, document, value)

    def test_data(self):
        document = """
            document: modulemd
            version: 0
            data: $VALUE
        """
        self.assertRaisesRegexp(ValueError, ".* is required",
                                self.test_object_missing, document)
        for value in ["", "unknown", "[]", "9999"]:
            self.assertRaisesRegexp(ValueError,
                                    ".* is required",
                                    self.test_object_value, document, value)

    def test_name(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: $VALUE
                version: 1.23
                release: 4
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError,
                                "name is required",
                                self.test_object_missing, document)
        for value in ["", "test", "[]", "{}", "1"]:
            self.test_object_value(document, value)

    def test_version(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: $VALUE
                release: 4
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError,
                                "version is required",
                                self.test_object_missing, document)
        for value in ["", "test", "[]", "{}", "1"]:
            self.test_object_value(document, value)

    def test_release(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23
                release: $VALUE
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError,
                                "release is required",
                                self.test_object_missing, document)
        for value in ["", "test", "[]", "{}", "1"]:
            self.test_object_value(document, value)

    def test_summary(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23
                release: 4
                summary: $VALUE
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError,
                                "summary is required",
                                self.test_object_missing, document)
        for value in ["", "test", "[]", "{}", "1"]:
            self.test_object_value(document, value)

    def test_description(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23
                release: 4
                summary: A test module
                description: $VALUE
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
        """
        self.assertRaisesRegexp(ValueError,
                                "description is required",
                                self.test_object_missing, document)
        for value in ["", "test", "[]", "{}", "1"]:
            self.test_object_value(document, value)

    def test_license(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23
                release: 4
                summary: A test module
                description: $VALUE
                license: $VALUE
        """
        self.assertRaisesRegexp(ValueError,
                                "description is required",
                                self.test_object_missing, document)

        values = ["", "test", "1", "[]", "{}"]
        values += ["{content:[MIT, GPL]}", "{module: []}"]
        values += ["{module: }", "{module: {}}"]

        for value in values:
            self.assertRaisesRegexp(ValueError,
                                    "at least one module license is required",
                                    self.test_object_value, document, value)

        self.test_object_value(document, "{module: [MIT]}")
        self.test_object_value(document, "{module: MIT}")

    def test_dependencies(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23
                release: 4
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                dependencies: $VALUE
        """
        self.test_object_missing(document)
        for value in ["", "test", "1", "[]", "{}"]:
            self.test_object_value(document, value)

    def test_dependencies_type(self):
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23
                release: 4
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                dependencies:
                    requires: $VALUE
        """
        self.test_object_value(document, "")
        self.test_object_value(document, "[]")
        self.test_object_value(document, "{}")
        self.assertRaisesRegexp(TypeError, "Incorrect data type passed",
            self.test_object_value, document, "[foo, bar]")
        self.test_object_value(document, "{modulemd: 42-42}")

if __name__ == "__main__":
    unittest.main()
