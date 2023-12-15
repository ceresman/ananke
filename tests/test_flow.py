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
from ananke.module import Module
from ananke.flow import Flow
from collections import Counter
from datetime import datetime

class TestModule(Module):
    def __init__(self, name):
        super().__init__(name=name)
        self.index=int(self.name[-1])
        self.ref_count = Counter()
        self.timestamp = None


    def forward(self, **kwargs):
        self.timestamp = datetime.now()
        kwargs["input_data"]["data"+str(self.index)]+=1
        data= kwargs["input_data"]
        self.logger.info(f"Processing {self.name} with data: {data} at {self.timestamp}")
        self.ref_count[self.index] += 1
        
__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"

def test_flow():
    #创建一个Flow实例
    flow = Flow(name="ComplexFlow")
    input_data={
        "data1": 0,
        "data2": 1,
        "data3": 2,
        "data4": 3,
        "data5": 4
    }

    # 创建五个TestModule实例
    module1 = TestModule("Module1")
    module2 = TestModule("Module2")
    module3 = TestModule("Module3")
    module4 = TestModule("Module4")
    module5 = TestModule("Module5")

    # 将模块添加到Flow中
    flow.add_module(module1)
    flow.add_module(module2)
    flow.add_module(module3)
    flow.add_module(module4)
    flow.add_module(module5)

    # 添加边以指定执行顺序
    flow.add_edge(module1, module2)
    flow.add_edge(module2, module3)
    flow.add_edge(module2, module4)
    flow.add_edge(module3, module5)
    flow.add_edge(module4, module5)

    # 执行Flow
    flow.execute(input_data=input_data)

    # 输出每个模块的引用计数
    for module_name, module in flow.modules.items():
        module.logger.info(f"{module_name}: {module.ref_count}")