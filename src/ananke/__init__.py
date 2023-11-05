import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package config
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError





# TODO : Implement a first level data type may be need as interface of @dataclass 

from ananke.base import BaseGraph,BaseRelation,BaseNode


class Node(BaseNode):
    def __init__(self, config):
        """
        Base Structure Interface of GraphNodes
        """
        super().__init__(config)
        
class Relation(BaseRelation):
    def __init__(self, config):
        """
        Base Structure Interface of GraphRelations
        """
        super().__init__(config)
        

class Graph(BaseGraph):
    def __init__(self,**kwargs):
        super().__init__()
        
        
        
from ananke.base import BaseStorage,BaseChunk,BaseVector


class Vector(BaseVector):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "Vector"
        self.logger.info(f"Initialized {self.type}.")
        
