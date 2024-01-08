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
from collections import Counter
from datetime import datetime
import threading
import time
from ananke.flow.info_flow import UserContextFlow
__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"


def test_flow():
    # 创建一个Flow实例
    flow = UserContextFlow()
    input_data = {"data1": 0, "data2": 1, "data3": 2, "data4": 3, "data5": 4}

    # 执行Flow
    flow.execute(input_data=input_data)
    flow.logger.debug(input_data)
