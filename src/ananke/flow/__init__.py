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


from ananke.base import BaseFlow,BaseModule
from abc import ABC,abstractmethod


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
    @abstractmethod
    def add_module(self, module):
        """
        Add a module to the information compression flow. Only instances of BaseModule can be added to the flow
        So , better to add code to check subclass like 
        ```python
        if not issubclass(module.__class__, BaseModule):
            raise ValueError("Only instances of BaseModule can be added to the flow.")
        module_name = module.name
        if module_name in self.modules:
            raise ValueError(f"Module with name '{module_name}' already exists in the flow.")
        self.modules[module_name] = module
        self.logger.info(f"Added module '{module_name}' to the flow.")
        ```
        Args:
            module (BaseModule): The module instance to add.

        Raises:
            ValueError: If the module is not a subclass of BaseModule.
        """
        pass

    @abstractmethod
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
        pass
    
        
    @abstractmethod    
    def del_module(self,module):
        """
        delete specific module in current flow

        Args:
            module (_type_): _description_
        """
        pass
        

    def show(self):
        """
        Show all modules in current flow
        """
        pass