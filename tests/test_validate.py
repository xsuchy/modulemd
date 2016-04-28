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

class TestValidate(unittest.TestCase):
    def setUp(self):
        self.mmd = modulemd.ModuleMetadata()
        self.mmd.load("tests/test.yaml")

    def test_validate_mdversion(self):
        self.mmd._mdversion = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_name(self):
        self.mmd._name = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_version(self):
        self.mmd._version = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_summary(self):
        self.mmd._summary = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_description(self):
        self.mmd._description = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_module_licenses1(self):
        self.mmd._module_licenses = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_module_licenses2(self):
        self.mmd._module_licenses = set([1, 2, 3])
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_content_licenses1(self):
        self.mmd._content_licenses = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_content_licenses2(self):
        self.mmd._content_licenses = set([1, 2, 3])
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_requires1(self):
        self.mmd._requires = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_requires2(self):
        self.mmd._requires = { "foo" : 1 }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_requires3(self):
        self.mmd._requires = { 1 : "foo" }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_requires4(self):
        self.mmd._requires = { 1 : 2 }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_community(self):
        self.mmd._community = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_documentation(self):
        self.mmd._documentation = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_tracker(self):
        self.mmd._tracker = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_components(self):
        self.mmd._components = None
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms(self):
        self.mmd.components._rpms = 1
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_dependencies(self):
        self.mmd.components.rpms._dependencies = 1
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_fulltree(self):
        self.mmd.components.rpms._fulltree = 1
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages1(self):
        self.mmd.components.rpms._packages = 1
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages2(self):
        self.mmd.components.rpms._packages = { "foo" : 1 }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages3(self):
        self.mmd.components.rpms._packages = { 1 : None }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages4(self):
        self.mmd.components.rpms._packages = { "foo" : { 1 : None } }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages5(self):
        self.mmd.components.rpms._packages = { "foo" : { "arches" : 1 } }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages6(self):
        self.mmd.components.rpms._packages = { "foo" : { "arches" : [1, 2, 3] } }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages7(self):
        self.mmd.components.rpms._packages = { "foo" : { "multilib" : 1 } }
        self.assertRaises(TypeError, self.mmd.validate)

    def test_validate_rpms_packages8(self):
        self.mmd.components.rpms._packages = { "foo" : { "multilib" : [1, 2, 3] } }
        self.assertRaises(TypeError, self.mmd.validate)

if __name__ == "__main__":
    unittest.main()
