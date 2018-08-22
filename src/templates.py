import json
from enum import Enum

# enum wrapper for Core and Module classes
class Component(Enum):
    core = 0
    module = 1

    def __init__(self, inner):
        self.inner = inner

    def inner(self):
        self.inner

class Core():
    pass

class Module:
    pass

# load components from package dir and return as ({"name": Component} [errors])
def load_from(package_dir):
    loaded = {}
    errors = []
    return (loaded, errors)