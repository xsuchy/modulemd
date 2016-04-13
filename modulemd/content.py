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
