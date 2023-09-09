# Copyright 2023 winshare
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


from ananke.base.base_object import BaseStorage


class ChromaStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.name = "ChromaStorage"
        self.logger.info(f"Initialized {self.name}.")
        
        
        
        
class Neo4jStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.name = "Neo4jStorage"
        self.logger.info(f"Initialized {self.name}.")
        
        
        
class RedisStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.name = "RedisStorage"
        self.logger.info(f"Initialized {self.name}.")
        


class SqliteStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.name = "SqliteStorage"
        self.logger.info(f"Initialized {self.name}.")
        
        
class NebulaStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.name = "NebulaStorage"
        self.logger.info(f"Initialized {self.name}.")
        
        
class MariaDBStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.name = "MariaDBStorage"
        self.logger.info(f"Initialized {self.name}.")
        
        
