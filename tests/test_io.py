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

class TestIO(unittest.TestCase):
    def test_load(self, filename="tests/test.yaml"):
        mmd = modulemd.ModuleMetadata()
        mmd.load(filename)
        self.assertEqual(mmd.mdversion, 0)
        self.assertEqual(mmd.name, "test")
        self.assertEqual(mmd.version, "1.23-1")
        self.assertEqual(mmd.summary, "A test module")
        self.assertEqual(mmd.description,
            "This module is a part of the modulemd test suite.")
        self.assertEqual(mmd.module_licenses, set(["MIT"]))
        self.assertEqual(mmd.content_licenses, set(["GPL+", "GPLv3"]))
        self.assertEqual(mmd.requires, {"modulemd" : "42-42"})
        self.assertEqual(mmd.community, "http://www.example.com/community")
        self.assertEqual(mmd.documentation, "http://www.example.com/documentation")
        self.assertEqual(mmd.tracker, "http://www.example.com/tracker")
        self.assertFalse(mmd.components.rpms.dependencies)
        self.assertFalse(mmd.components.rpms.fulltree)
        self.assertEqual(mmd.components.rpms.packages,
            { "alfa" : None,
              "bravo" : { "arches" : [ "charlie", "delta" ],
                          "multilib" : [ "echo" ] } } )

    def test_loads(self, yaml=None):
        mmd = modulemd.ModuleMetadata()
        document = """
            document: modulemd
            version: 0
            data:
                name: test
                version: 1.23-1
                summary: A test module
                description: >
                    This module is a part of the modulemd test suite.
                license:
                    module: [ MIT ]
                    content: [ GPL+, GPLv3 ]
                requires: { modulemd: 42-42 }
                references:
                    community: http://www.example.com/community
                    documentation: http://www.example.com/documentation
                    tracker: http://www.example.com/tracker
                components:
                    rpms:
                        dependencies: False
                        fulltree: False
                        packages:
                            alfa: ~
                            bravo:
                                arches: [ charlie, delta ]
                                multilib: [ echo ]
        """
        if not yaml:
            yaml = document
        mmd.loads(yaml)
        self.assertEqual(mmd.mdversion, 0)
        self.assertEqual(mmd.name, "test")
        self.assertEqual(mmd.version, "1.23-1")
        self.assertEqual(mmd.summary, "A test module")
        self.assertEqual(mmd.description,
            "This module is a part of the modulemd test suite.")
        self.assertEqual(mmd.module_licenses, set(["MIT"]))
        self.assertEqual(mmd.content_licenses, set(["GPL+", "GPLv3"]))
        self.assertEqual(mmd.requires, {"modulemd" : "42-42"})
        self.assertEqual(mmd.community, "http://www.example.com/community")
        self.assertEqual(mmd.documentation, "http://www.example.com/documentation")
        self.assertEqual(mmd.tracker, "http://www.example.com/tracker")
        self.assertFalse(mmd.components.rpms.dependencies)
        self.assertFalse(mmd.components.rpms.fulltree)
        self.assertEqual(mmd.components.rpms.packages,
            { "alfa" : None,
              "bravo" : { "arches" : [ "charlie", "delta" ],
                          "multilib" : [ "echo" ] } } )

    def test_dump(self):
        mmd = modulemd.ModuleMetadata()
        mmd.mdversion = 0
        mmd.name = "test"
        mmd.version = "1.23-1"
        mmd.summary = "A test module"
        mmd.description = "This module is a part of the modulemd test suite."
        mmd.add_module_license("MIT")
        mmd.add_content_license("GPL+")
        mmd.add_content_license("GPLv3")
        mmd.add_requires("modulemd", "42-42")
        mmd.community = "http://www.example.com/community"
        mmd.documentation = "http://www.example.com/documentation"
        mmd.tracker = "http://www.example.com/tracker"
        mmd.components = modulemd.ModuleComponents()
        mmd.components.rpms = modulemd.ModuleRPMs()
        mmd.components.rpms.dependencies = False
        mmd.components.rpms.fulltree = False
        mmd.components.rpms.add_package("alfa")
        mmd.components.rpms.add_package("bravo",
            arches=["charlie", "delta"], multilib=["echo"])
        mmd.dump("tests/dump.yaml")
        self.test_load(filename="tests/dump.yaml")

    def test_dumps(self):
        mmd = modulemd.ModuleMetadata()
        mmd.mdversion = 0
        mmd.name = "test"
        mmd.version = "1.23-1"
        mmd.summary = "A test module"
        mmd.description = "This module is a part of the modulemd test suite."
        mmd.add_module_license("MIT")
        mmd.add_content_license("GPL+")
        mmd.add_content_license("GPLv3")
        mmd.add_requires("modulemd", "42-42")
        mmd.community = "http://www.example.com/community"
        mmd.documentation = "http://www.example.com/documentation"
        mmd.tracker = "http://www.example.com/tracker"
        mmd.components = modulemd.ModuleComponents()
        mmd.components.rpms = modulemd.ModuleRPMs()
        mmd.components.rpms.dependencies = False
        mmd.components.rpms.fulltree = False
        mmd.components.rpms.add_package("alfa")
        mmd.components.rpms.add_package("bravo",
            arches=["charlie", "delta"], multilib=["echo"])
        self.test_loads(yaml=mmd.dumps())

if __name__ == "__main__":
    unittest.main()
