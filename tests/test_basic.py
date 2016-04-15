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
# Written by Petr Šabata <contyk@redhat.com>

import unittest

import os
import sys

DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(DIR, ".."))

import modulemd

class TestBasic(unittest.TestCase):
    def setUp(self):
        self.mmd = modulemd.ModuleMetadata()
        self.mmd.name = "test"
        self.mmd.version = "42-1"
        self.mmd.summary = "A test module"
        self.mmd.description = "It's only used for testing purposes."
        self.mmd.module_licenses = set([ "MIT" ])
        self.mmd.content_licenses = set([ "ISC" ])
        self.mmd.requires = { "dependency" : "1.00-1" }
        self.mmd.community = "http://www.example.com/community"
        self.mmd.documentation = "http://www.example.com/documentation"
        self.mmd.tracker = "http://www.example.com/tracker"
        self.mmd.components = modulemd.ModuleComponents()
        self.mmd.components.rpms = modulemd.ModuleRPMs()
        self.mmd.components.rpms.dependencies = False
        self.mmd.components.rpms.fulltree = False
        self.mmd.components.rpms.packages = { "rpm" : None }

    def test_mdversion(self):
        self.assertIn(self.mmd.mdversion, modulemd.supported_mdversions)

    def test_name(self):
        self.assertEqual(self.mmd.name, "test")

    def test_version(self):
        self.assertEqual(self.mmd.version, "42-1")

    def test_summary(self):
        self.assertEqual(self.mmd.summary, "A test module")

    def test_description(self):
        self.assertEqual(self.mmd.description, "It's only used for testing purposes.")

    def test_module_licenses(self):
        self.assertEqual(self.mmd.module_licenses, set(["MIT"]))

    def test_content_licenses(self):
        self.assertEqual(self.mmd.content_licenses, set(["ISC"]))

    def test_requires(self):
        self.assertEqual(self.mmd.requires, {"dependency" : "1.00-1"})

    def test_community(self):
        self.assertEqual(self.mmd.community, "http://www.example.com/community")

    def test_documentation(self):
        self.assertEqual(self.mmd.documentation, "http://www.example.com/documentation")

    def test_tracker(self):
        self.assertEqual(self.mmd.tracker, "http://www.example.com/tracker")

    def test_components(self):
        self.assertIsInstance(self.mmd.components, modulemd.ModuleComponents)

    def test_rpms(self):
        self.assertIsInstance(self.mmd.components.rpms, modulemd.ModuleRPMs)

    def test_rpm_dependencies(self):
        self.assertFalse(self.mmd.components.rpms.dependencies)

    def test_rpm_fulltree(self):
        self.assertFalse(self.mmd.components.rpms.fulltree)

    def test_rpm_packages(self):
        self.assertEqual(self.mmd.components.rpms.packages, { "rpm" : None })

if __name__ == "__main__":
    unittest.main()
