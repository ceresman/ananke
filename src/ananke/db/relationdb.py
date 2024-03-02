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

from ananke.db import relation_storage


class RedisStorage(relation_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "RedisStorage"
        self.logger.info(f"Initialized {self.type}.")
        


class SqliteStorage(relation_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "SqliteStorage"
        self.logger.info(f"Initialized {self.type}.")
        
    
        
class MariaDBStorage(relation_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "MariaDBStorage"
        self.logger.info(f"Initialized {self.type}.")
        
        
