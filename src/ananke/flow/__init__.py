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

from ananke.base import BaseFlow
from ananke.module import Module
from abc import ABC, abstractmethod
import logging
import networkx as nx
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

class Flow(BaseFlow):
    def __init__(self, **kwargs):
        """
        Initialize the information compression flow.

        Args:
            **kwargs: Optional arguments.
        """
        super().__init__(**kwargs)
        self.name = "Flow"  # Default value
        if 'name' in kwargs:
            self.name = kwargs['name']
            self.logger.info(f"Initialized {self.name}.")
        else:
            self.logger.info("Initialized Flow without specifying a name.")
        self.graph = nx.DiGraph()
        self.module_outputs = {}  # 存储每个模块的输出

    def add_module(self, module: Module, index=None):
        """
        Add a module to the information compression flow.

        Args:
            module (Module): The module instance to add.
            index (int): The index of insert position in process sequence

        Raises:
            ValueError: If the module is not a subclass of Module or the module with the same name already exists in the flow.
        """
        if not issubclass(module.__class__, Module):
            raise ValueError("Only instances of Module can be added to the flow.")
        module_name = module.name
        if module_name in self.graph.nodes():
            raise ValueError(f"Module with name '{module_name}' already exists in the flow.")
        self.graph.add_node(module_name)
        self.modules[module_name] = module
        self.logger.info(f"Added module '{module_name}' to the flow.")

    def execute(self, **kwargs):
        """
        Execute the information compression flow by processing the added modules in topological order.
        """
        sorted_nodes = list(nx.topological_sort(self.graph))
        self.logger.info(f"Executing flow in topological order: {sorted_nodes}")

        for module_name in sorted_nodes:
            module = self.modules[module_name]
            input_data = self._get_input_data(module_name, kwargs)
            
            try:
                output = module.forward(**input_data)
                self.module_outputs[module_name] = output
                self.logger.info(f"Module '{module_name}' executed successfully.")
            except Exception as e:
                self.logger.error(f"Module '{module_name}' failed to execute: {e}")
                raise

        return self.module_outputs[sorted_nodes[-1]]  # 返回最后一个模块的输出

    def _get_input_data(self, module_name, global_inputs):
        """
        获取模块的输入数据。
        """
        input_data = {}
        for predecessor in self.graph.predecessors(module_name):
            input_data.update(self.module_outputs[predecessor])
        input_data.update(global_inputs)
        return input_data

    def add_edge(self, source: Module, target: Module):
        """
        Add an edge between two modules in the flow.

        Args:
            source (Module): The name of the source module.
            target (Module): The name of the target module.
        """
        self.graph.add_edge(source.name, target.name)

    def remove_node(self, name):
        """
        Remove a module from the flow.

        Args:
            name (str): The name of the module to remove.
        """
        self.graph.remove_node(name)
        if name in self.modules:
            del self.modules[name]
        if name in self.module_outputs:
            del self.module_outputs[name]

    def get_module(self, name):
        """
        获取指定名称的模块。
        """
        return self.modules.get(name)

    def get_module_output(self, name):
        """
        获取指定模块的输出。
        """
        return self.module_outputs.get(name)

    def visualize(self):
        """
        可视化计算图。
        """
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', 
                node_size=1500, font_size=10, font_weight='bold')
        plt.title("Flow Computation Graph")
        plt.show()

    def save_graph(self, filename):
        """
        保存计算图到文件。
        """
        nx.write_gpickle(self.graph, filename)

    def load_graph(self, filename):
        """
        从文件加载计算图。
        """
        self.graph = nx.read_gpickle(filename)

    def clear(self):
        """
        清空计算图和所有模块。
        """
        self.graph.clear()
        self.modules.clear()
        self.module_outputs.clear()

    def show(self, debug=False):
        """
        Print all modules with their order in the process sequence. If debug is True, print data as well.

        Args:
            debug (bool): Whether to print data or not.
        """
        sorted_nodes = list(nx.topological_sort(self.graph))
        print(f"Modules in topological order:")
        for i, module_name in enumerate(sorted_nodes):
            print(f"{i+1}. {module_name}")
            if debug:
                module = self.modules[module_name]
                print(f"   Input shape: {module.input_shape}")
                print(f"   Output shape: {module.output_shape}")
                if module_name in self.module_outputs:
                    print(f"   Output data: {self.module_outputs[module_name]}")
            print()

    def _analyze_parallel_dependencies(self, sorted_nodes):
        """
        分析计算图的并行依赖关系。

        Args:
            sorted_nodes: 计算图的拓扑排序。

        Returns:
            并行组列表。
        """
        # TODO: 实现更高效的并行依赖分析算法
        parallel_groups = [[node] for node in sorted_nodes]
        return parallel_groups
    
    
