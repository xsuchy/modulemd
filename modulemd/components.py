from modulemd.rpms import ModuleRPMs

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
