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
import time
import threading
from ananke.module import Module
from ananke.flow import Flow

class TestModule(Module):
    def __init__(self, name):
        super().__init__(name=name)
        self.index = int(self.name[-1])
        self.timestamp = None

    def forward(self, **kwargs):
        self.current_thread = threading.get_ident()
        self.timestamp = time.time()
        
        input_data = kwargs.get("input_data", {})
        input_data[f"data{self.index}"] = input_data.get(f"data{self.index}", 0) + 1
        input_data[f"data{self.index}time"] = self.timestamp
        input_data[f"data{self.index}threading"] = self.current_thread
        
        return {"output": input_data}

def test_flow():
    # 创建一个Flow实例
    flow = Flow(name="ComplexFlow")
    input_data = {
        "data1": 0,
        "data2": 1,
        "data3": 2,
        "data4": 3,
        "data5": 4
    }

    # 创建五个TestModule实例
    modules = [TestModule(f"Module{i}") for i in range(1, 6)]

    # 将模块添加到Flow中
    for module in modules:
        flow.add_module(module)

    # 添加边以指定执行顺序
    flow.add_edge(modules[0], modules[1])
    flow.add_edge(modules[0], modules[2])
    flow.add_edge(modules[0], modules[3])
    flow.add_edge(modules[0], modules[4])

    # 执行Flow
    result = flow.execute(input_data=input_data)

    # 验证结果
    assert "output" in result
    output = result["output"]
    
    # 检查每个模块是否正确处理了数据
    for i in range(1, 6):
        assert f"data{i}" in output
        assert output[f"data{i}"] == input_data[f"data{i}"] + (1 if i == 1 else 0)
        assert f"data{i}time" in output
        assert f"data{i}threading" in output

    # 检查模块执行顺序
    assert output["data1time"] < min(output[f"data{i}time"] for i in range(2, 6))

    # 测试获取模块和模块输出
    for i in range(1, 6):
        module = flow.get_module(f"Module{i}")
        assert module is not None
        assert isinstance(module, TestModule)

        module_output = flow.get_module_output(f"Module{i}")
        assert module_output is not None
        assert "output" in module_output

    # 测试移除节点
    flow.remove_node("Module5")
    assert "Module5" not in flow.modules
    assert "Module5" not in flow.module_outputs
    assert "Module5" not in flow.graph.nodes()

    # 测试清空Flow
    flow.clear()
    assert len(flow.modules) == 0
    assert len(flow.module_outputs) == 0
    assert len(flow.graph.nodes()) == 0

    # 注意：可视化、保存和加载图的测试可能需要在集成测试中进行，因为它们涉及文件I/O和图形界面

if __name__ == "__main__":
    pytest.main([__file__])