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
import logging
from colorlog import ColoredFormatter

class BaseObject(ABC):
    """Base class for all objects in Ananke."""

    def __init__(self, name):
        self.name = name
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

# class YourSubclass(BaseObject):
#     def __init__(self, name):
#         super().__init__(name)

# if __name__ == "__main__":
#     # Create an instance of YourSubclass and pass a name
#     obj = YourSubclass("TestObject")
    
#     # Log some messages at different levels
#     obj.logger.debug("This is a debug message.")
#     obj.logger.info("This is an info message.")
#     obj.logger.warning("This is a warning message.")
#     obj.logger.error("This is an error message.")
#     obj.logger.critical("This is a critical message.")

