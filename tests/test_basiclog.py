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
import pytest
from ananke.base import BaseObject

__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"


class YourSubclass(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
def test_your_subclass_logging():
    obj = YourSubclass(name="TestObject")
    # assert obj.name == "TestObject"
    
    # 检查是否正确设置了 logger
    # assert obj.logger.name == "TestObject"
    
    # 检查是否能够正常记录不同级别的日志
    obj.logger.debug("This is a debug message.")
    obj.logger.info("This is an info message.")
    obj.logger.warning("This is a warning message.")
    obj.logger.error("This is an error message.")
    obj.logger.critical("This is a critical message.")