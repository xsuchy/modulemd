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

class TestRequires(unittest.TestCase):
    def setUp(self):
        self.mmd = modulemd.ModuleMetadata()

    def test_add_requires(self):
        self.mmd.requires = dict()
        self.mmd.add_requires("AddName", "AddVersion")
        self.assertEqual(self.mmd.requires, { "AddName" : "AddVersion" })

    def test_update_requires(self):
        self.mmd.requires = dict()
        self.mmd.update_requires("UpdateName", "UpdateVersion")
        self.assertEqual(self.mmd.requires, { "UpdateName" : "UpdateVersion" })
        self.mmd.update_requires("UpdateName", "UpdateVersion-1")
        self.assertEqual(self.mmd.requires, { "UpdateName" : "UpdateVersion-1" })

    def test_del_requires(self):
        self.mmd.requires = { "DelName" : "DelVersion" }
        self.mmd.del_requires("DelName")
        self.assertEqual(self.mmd.requires, dict())

    def test_clear_requires(self):
        self.mmd.requires = { "ClearName" : "ClearVersion" }
        self.mmd.clear_requires()
        self.assertEqual(self.mmd.requires, dict())

if __name__ == "__main__":
    unittest.main()
