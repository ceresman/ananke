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

from ananke.base import BaseModule


class LLMGraphGenerator(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "LLMGraphGenerator"
        self.logger.info(f"Initialized {self.name}.")
        
        
        
class EmebeddingGenerator(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "EmebeddingGenerator"
        self.logger.info(f"Initialized {self.name}.")
        
        
class RepresentationConstructor(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "RepresentationConstructor"
        self.logger.info(f"Initialized {self.name}.")
        
        
        
class Syncer(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Syncer"
        self.logger.info(f"Initialized {self.name}.")
        
class Preprocessor(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Preprocessor"
        self.logger.info(f"Initialized {self.name}.")
        
class Serializer(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Serializer"
        self.logger.info(f"Initialized {self.name}.")


        
class CustomModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "CustomModule"
        self.logger.info(f"Initialized {self.name}.")
        
