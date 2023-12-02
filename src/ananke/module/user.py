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

from typing import Any,List
from ananke.module import Module,Context
from ananke.flow import Flow
class Intention(Module):
    def __init__(self, name, description, author, version, dependencies):
        super().__init__(name, description, author, version, dependencies)
        self.structured_intention=None
        self.actions = List[Module]
    
    def parse(self,intention_context):
        return intention_context

    def __call__(self, data: Context, **kwargs: Any) -> Any:
        data=self.parse(data)
        return data
    
class IntentionExecutor(Flow):
    def __init__(self,Intention:Intention):
        super().__init__(Intention)


    
class IntentionEvaluator(Flow):
    def __init__(self,Intention:Intention,Result:Context):
        super().__init__(Intention,Result)
           