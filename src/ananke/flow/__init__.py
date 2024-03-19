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
from abc import ABC,abstractmethod

import logging
import networkx as nx
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    def add_module(self, module: Module, index=None):
        """
        Add a module to the information compression flow. Only instances of Module can be added to the flow
        So , better to add code to check subclass like 
        ```python
        if not issubclass(module.__class__, Module):
            raise ValueError("Only instances of Module can be added to the flow.")
        module_name = module.name
        if module_name in self.graph.nodes():
            raise ValueError(f"Module with name '{module_name}' already exists in the flow.")
        self.graph.add_node(module_name)
        self.logger.info(f"Added module '{module_name}' to the flow.")
        ```
        Args:
            module (Module): The module instance to add.
            index (int): The index of insert position in process sequence

        Raises:
            ValueError: If the module is not a subclass of Module.
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
        Execute the information compression flow by processing the added modules sequentially.
        here is a sample to execute each module in queue
        ```python
        for name, module in self.modules.items():
        self.logger.info(f"Executing module '{name}'...")
        module.init(**kwargs)
        module.forward(**kwargs)
        self.logger.info(f"Module '{name}' executed successfully.")
        ```
        Args:
            **kwargs: Input parameters.
        """
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.modules[module_name].forward, **kwargs): module_name for module_name in self.graph.nodes()}
            for future in as_completed(futures):
                module_name = futures[future]
                try:
                    future.result()
                    self.logger.info(f"Module '{module_name}' executed successfully.")
                except Exception as e:
                    self.logger.error(f"Module '{module_name}' failed to execute: {e}")

    def add_edge(self, source : Module, target:Module):
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

    def show(self, debug=False):
        """
        print all module with order in process sequence.
        if debug , print data same time. 
        """
        pass