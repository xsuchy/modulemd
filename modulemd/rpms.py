from modulemd.content import ModuleContent

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

        update_package = add_package

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
