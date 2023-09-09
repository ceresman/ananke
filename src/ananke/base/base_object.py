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
from abc import ABC
from ananke.base.config import CONFIG_TEMPLATE
from colorlog import ColoredFormatter
import logging


# ---------------------------------------------------------------------------- #
#                               System Operation                               #
# ---------------------------------------------------------------------------- #


class BaseLogger(ABC):
    def __init__(self):
        self.logger = self.setup_logger()


    def setup_logger(self):
        logger = logging.getLogger(self.name)
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


class InstructLogger(BaseLogger):
    """Base log class for all instruct objects in Ananke."""
    def __init__(self,name):
        self.name = name
        super().__init__()


class BaseConfig(ABC):
    """Base class for all config objects in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger


class InstructConfig(BaseConfig):
    """Base class for all instruct config objects in Ananke."""
    def __init__(self, name):
        super().__init__(name)
        self.config_template = CONFIG_TEMPLATE
    



# ---------------------------------------------------------------------------- #
#                             Basic Data Structure                             #
# ---------------------------------------------------------------------------- #




class BaseObject(ABC):
    """Base class for all objects in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger


class BaseChunk(ABC):
    """Base class for all chunks in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger

class BaseDocument(ABC):
    """Base class for all documents in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        
class BaseMeta(ABC):
    """Base class for all meta in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger


class BaseGraph(ABC):
    """Base class for all graphs in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger

class BaseNode(ABC):
    """Base class for all nodes in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger

class BaseRelation(ABC):
    """Base class for all relations in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger

class BaseVector(ABC):
    """Base class for all vectors in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger


class BaseMedia(ABC):
    """Base class for all media in Ananke."""

    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        

class BaseFile(ABC):
    """Base class for all files in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger



# ---------------------------------------------------------------------------- #
#                          IO & Storage & LLM & Prompt                         #
# ---------------------------------------------------------------------------- #



class BaseStorage(ABC):
    """Base class for all storage in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        
        
class BaseLocalLLM(ABC):
    """Base class for all Local LLM in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        
class BaseRemoteLLM(ABC):
    """Base class for all Remote LLM in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger


class BasePrompt(ABC):
    """Base class for all prompts in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        




# ---------------------------------------------------------------------------- #
#                              INFO Module & Flow                              #
# ---------------------------------------------------------------------------- #



class BaseModule(ABC):
    """Base class for all modules in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger



class BaseFlow(ABC):
    """Base class for all info compression in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        
        


# ---------------------------------------------------------------------------- #
#                                Plugins & Utils                               #
# ---------------------------------------------------------------------------- #


class BasePlugin(ABC):
    """Base class for all plugins in Ananke."""
    def __init__(self, name):
        self.name = name
        
        
class BaseUtils(ABC):
    """Base class for all utils in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        
        
class BaseServer(ABC):
    """Base class for all servers in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger
        
class BaseClient(ABC):
    """Base class for all clients in Ananke."""
    def __init__(self, name):
        self.name = name
        self.instruct = InstructLogger(name)
        self.logger = self.instruct.logger