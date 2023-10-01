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

from ananke.base import BaseStorage


class vector_storage(BaseStorage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "vector_storage"
        self.logger.info(f"Initialized {self.type}.")
        
class kg_storage(BaseStorage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "kg_storage"
        self.logger.info(f"Initialized {self.type}.")
        
class relation_storage(BaseStorage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "relation_storage"
        self.logger.info(f"Initialized {self.type}.")