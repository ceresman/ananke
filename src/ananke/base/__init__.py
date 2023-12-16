# Copyright 2023 undefined
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from abc import ABC,abstractmethod
from colorlog import ColoredFormatter
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from collections import OrderedDict
import logging
import platform
import os

# ---------------------------------------------------------------------------- #
#                               System Operation                               #
# ---------------------------------------------------------------------------- #
from ananke.base.config import YAMLCONFIG




class BaseObject(ABC):
    def __init__(self, **kwargs):
        self.config = YAMLCONFIG()
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(self.__class__.__name__)  # 使用当前类的名称作为日志名称
        logger.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger


    def get_system_info(self):
        system = platform.system()
        architecture = platform.architecture()[0]
        self.system=system
        self.architecture=architecture
        
        if system == "Windows":
            return f"Windows {architecture}"
        elif system == "Darwin":
            return f"macOS {architecture}"
        elif system == "Linux":
            distro = ""
            # Linux Release（Debian、CentOS、Ubuntu etc）
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("ID="):
                            distro = line.strip().split("=")[1].strip('"')
                            break
            return f"Linux ({distro}) {architecture}"
        else:
            return "Unrecognized System Label"


# ---------------------------------------------------------------------------- #
#                             Basic Data Structure                             #
# ---------------------------------------------------------------------------- #
class BaseContext(BaseObject):
    """Base class for all Context in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()

class BaseLogical(BaseObject):
    def __init__(self,**kwargs):
        super().__init__()

class BaseMath(BaseObject):
    def __init__(self,**kwargs):
        super().__init__()

class BaseSentence(BaseObject):
    """Base class for all sentence in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
        self.sentece_id = ""
        self.sentece_text = ""
        self.embedding_id:long = 0
        self.sentece_math: BaseMath = None
        self.sentece_logical: BaseLogical = None

class BaseChunk(BaseObject):
    """Base class for all chunks in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        self.chunk_id = ""
        self.chunk_text = ""
        self.embedding_id:long = 0
        self.sentences: List[BaseSentence] = None
        self.chunk_graph: BaseGraph = None
        self.chunk_logical: BaseLogical = None
        self.chunk_math: BaseMath = None

class BaseDocument(BaseObject):
    """Base class for all documents in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        self.logger.debug(">>Document Init with : "+str(self.__class__.__name__))
        self.document_id = ""
        self.document_text = ""
        self.chunks:List[BaseChunk] = None
        self.chunk_emb_collection = None
        self.sentence_emb_collection = None

# class BaseTriple(BaseObject):
#     """Base class for all documents in Ananke."""

#     def __init__(self,**kwargs):
#         super().__init__()
#         self.logger.debug(">>Document Init with : "+str(self.__class__.__name__))
#         self.document_id = ""
#         self.document_text = ""
#         self.chunks:List[BaseChunk] = None
#         self.chunk_emb_collection = None
#         self.sentence_emb_collection = None


class BaseMeta(BaseObject):
    """Base class for all meta in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()


class BaseNode(BaseObject):
    """Base class for all nodes in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        self.node_name : str = ""
        self.node_type : str = ""
        self.node_uuid : str = ""
        self.property : dict = {}

class BaseRelation(BaseObject):
    """Base class for all relations in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        self.relation_name : str = ""
        self.relation_type : str = ""
        self.relation_uuid : str = ""

class BaseGraph(BaseObject):
    """Base class for all graphs in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        self.nodes  = []

class BaseVector(BaseObject):
    """Base class for all vectors in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()


class BaseMedia(BaseObject):
    """Base class for all media in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        

class BaseFile(BaseObject):
    """Base class for all files in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()



# ---------------------------------------------------------------------------- #
#                          IO & Storage & LLM & Prompt                         #
# ---------------------------------------------------------------------------- #



class BaseStorage(BaseObject):
    """Base class for all storage in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
        
        
class BaseLocalLLM(BaseObject):
    """Base class for all Local LLM in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
        
class BaseRemoteLLM(BaseObject):
    """Base class for all Remote LLM in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()


class BasePrompt(BaseObject):
    """Base class for all prompts in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
    @abstractmethod
    def forward(self, **kwargs):
        """
        Forward prompt.
        """
        pass
    @abstractmethod
    def init(self, **kwargs):
        """
        Init prompt.
        """
        pass
# ---------------------------------------------------------------------------- #
#                              INFO Module & Flow                              #
# ---------------------------------------------------------------------------- #

# The Module is basic unit of info compression in Ananke. 
# The Flow that consist of list of Module is the basic unit of info flow in Ananke.

class BaseModule(BaseObject):
    """Base class for all modules in the Ananke framework."""
    def __init__(self, **kwargs):
        """
        Initialize the module.

        Args:
            **kwargs: Optional arguments.
        """
        super().__init__()


class BaseFlow(BaseObject):
    """Base class for all information compression flows in the Ananke framework."""
    def __init__(self, **kwargs):
        """
        Initialize the information compression flow.

        Args:
            **kwargs: Optional keyword arguments.

        Attributes:
            modules (OrderedDict): An ordered dictionary to store modules.
        """
        super().__init__()
        self.modules = OrderedDict()



# ---------------------------------------------------------------------------- #
#                                Plugins & Utils                               #
# ---------------------------------------------------------------------------- #


class BasePlugin(BaseObject):
    """Base class for all plugins in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
             
class BaseUtils(BaseObject):
    """Base class for all utils in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
        
        
class BaseServer(BaseObject):
    """Base class for all servers in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
        
class BaseClient(BaseObject):
    """Base class for all clients in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()