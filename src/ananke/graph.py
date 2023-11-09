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

from ananke.base import BaseGraph,BaseRelation,BaseNode

class Neo4JGraph(BaseGraph):
    def __init__(self,**kwargs):
        # TODO ： Add Neo4J Server Support
        super().__init__()
        self._driver = None
        self._session = None
        self.logger.info(f"Initialized {self.__class__.__name__}.")

    def __del__(self):
        self.close()
    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None
        if self._session:
            self._session.close()
            self._session = None


class NebulaGraph(BaseGraph):
    def __init__(self,**kwargs):
        # TODO : Add Nebular Server Support
        super().__init__()
        self._driver = None
        self._session = None
        self.logger.info(f"Initialized {self.__class__.__name__}.")

      
    def __del__(self):
        self.close()
    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None
        if self._session:
            self._session.close()
            self._session = None
            

# ---------------------------------------------------------------------------- #
#                              DATA TYPE INTERFACE                             #
# ---------------------------------------------------------------------------- #


