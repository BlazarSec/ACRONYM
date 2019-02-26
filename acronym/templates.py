"""
Contains component abstractions and provides translation between abstractions and real packages
"""

import json
from enum import Enum, auto

class Kind(Enum):
    CORE = auto()
    MODULE = auto()

# wrapper for Core and Module classes
class Component():
    def __init__(self, kind, inner):
        self.kind = kind
        self.inner = inner

class Core():
    pass

class Module:
    pass

# load components from package dir and return as ({"name": Component} [errors])
def load_pkgs(pkg_dir):
    loaded = {}
    errors = []

    # creation of Core/Module objects in memory, wrapped by Component
    # ex: Component(Kind.CORE, some_core) || Component(Kind.MODULE, some_module)

    return (loaded, errors)