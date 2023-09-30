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
import logging


# ---------------------------------------------------------------------------- #
#                               System Operation                               #
# ---------------------------------------------------------------------------- #



class BaseConfig():
    """Base class for all config objects in Ananke."""
    def __init__(self, **kwargs):
        pass

class YAMLCONFIG(BaseConfig):
    def __init__(self,**kwargs):
        super().__init__()

class BaseObject(ABC):
    def __init__(self, **kwargs):
        # self.config = YAMLCONFIG(config)
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





# ---------------------------------------------------------------------------- #
#                             Basic Data Structure                             #
# ---------------------------------------------------------------------------- #






class BaseChunk(BaseObject):
    """Base class for all chunks in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()

class BaseDocument(BaseObject):
    """Base class for all documents in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()
        self.logger.debug(">>Document Init with : "+str(self.__class__.__name__))
        
    @abstractmethod
    def read(self,**kwargs):
        pass
    @abstractmethod
    def write(self,**kwargs):
        pass
    
    def close(self):
        pass
        
class BaseMeta(BaseObject):
    """Base class for all meta in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()


class BaseGraph(BaseObject):
    """Base class for all graphs in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()

class BaseNode(BaseObject):
    """Base class for all nodes in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()

class BaseRelation(BaseObject):
    """Base class for all relations in Ananke."""

    def __init__(self,**kwargs):
        super().__init__()

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
    """Base class for all modules in Ananke."""
    def __init__(self,**kwargs):
        super().__init__()
        
    @abstractmethod
    def forward(self, **kwargs):
        """
        Module forward process logic interface.
        """
        pass
    @abstractmethod
    def init(self, **kwargs):
        """
        Module Init process interface.
        """
        pass


class BaseFlow(BaseObject):
    """Base class for all info compression in Ananke."""
    def __init__(self, config):
        
        super().__init__(config)
    
    
    @abstractmethod
    def init(self, **kwargs):
        """
        Flow init process interface.
        """
        pass
    @abstractmethod
    def forward(self, **kwargs):
        """
        Flow forward process interface.
        """
        pass
        

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